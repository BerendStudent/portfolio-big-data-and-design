from flask import Flask, request, render_template, redirect, url_for, make_response
import pandas as pd
from markupsafe import escape
import folium
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point
import json
from pathlib import Path

app = Flask(__name__)

CSV_PATH = "startup/app/points.csv"


def getPoints():
    return pd.read_csv(CSV_PATH)


def placePoint(lat, lon, description):
    df = pd.read_csv(CSV_PATH)
    df.loc[len(df)] = [lat, lon, description]
    df.to_csv(CSV_PATH, index=False)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_point", methods=["POST"])
def add_point():
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    description = request.form.get("description")

    if not lat or not lon or not description:
        return "Missing data", 400

    placePoint(lat, lon, description)

    return redirect("/")

@app.route("/reset_map", methods=["POST"])
def reset_map():
    mapObj = folium.Map(
        location=[52.081730, 5.104691],
        zoom_start=10
    )

    points = getPoints()

    for point in points.itertuples(index=False):
        markerObj = folium.Marker(
            location=[point.lat, point.lon],
            popup=f"<b>{point.description}</b>"
        )
        markerObj.add_to(mapObj)
    
    mapObj.save("startup/app/static/berlin_map.html")

    return ("", 204)

# Code van Gerjan
def create_safe_route_map(
    city_query: str,
    travel_mode: str,
    start_latlon: tuple[float, float],
    end_latlon: tuple[float, float],
    avoid_radius_m: float,
    penalty_multiplier: float,
    output_html: str = "startup/app/static/berlin_map.html",
    ):
    """
    city_query: bijv. "Utrecht, Netherlands"
    travel_mode: "walk", "bike", of "drive"
    start_latlon / end_latlon: (lat, lon)
    avoid_latlon_list: lijst van punten die je wilt vermijden
    avoid_radius_m: binnen deze afstand -> penalty
    penalty_multiplier: hoe "onaantrekkelijk" (hoger = meer vermijden)
    """

    # OSMnx instellingen (cache is fijn voor herhaald testen)
    ox.settings.use_cache = True
    ox.settings.log_console = False

    # import points csv
    df = pd.read_csv("startup/app/points.csv")

    avoid_latlon_list = list(zip(df["lat"], df["lon"]))


    
    # 1) Wegennet downloaden
    # We gebruiken 2 grafen:
    # - projected_graph (meters) om afstanden/penalty's te berekenen
    # - wgs_graph (lat/lon) om coördinaten te exporteren naar JSON en voor folium
    projected_graph = ox.graph_from_place(city_query, network_type=travel_mode)
    projected_graph = ox.project_graph(projected_graph)

    wgs_graph = ox.graph_from_place(city_query, network_type=travel_mode)

    
    # 2) Start/eind omzetten naar dichtstbijzijnde nodes in de graaf
    start_node_id = ox.distance.nearest_nodes(
        wgs_graph,
        X=start_latlon[1],  # lon
        Y=start_latlon[0],  # lat
    )
    end_node_id = ox.distance.nearest_nodes(
        wgs_graph,
        X=end_latlon[1],
        Y=end_latlon[0],
    )

    # 3) Avoid-punten projecteren (zodat we in meters kunnen meten)
    nodes_gdf = ox.graph_to_gdfs(projected_graph, nodes=True, edges=False)

    avoid_points_gdf = gpd.GeoDataFrame(
    df[["lat", "lon"]].assign(id=range(len(df))),
    geometry=gpd.points_from_xy(df["lon"], df["lat"]),
    crs="EPSG:4326",
    ).to_crs(nodes_gdf.crs)

    
    # 4) Voor elke weg (edge) bepalen hoe dicht hij bij avoid-punten ligt
    edges_gdf = ox.graph_to_gdfs(projected_graph, nodes=False, edges=True).copy()

    # min afstand (in meters) van edge naar dichtstbijzijnde avoid-punt
    min_distance_to_avoid = []
    if len(avoid_points_gdf) == 0:
        min_distance_to_avoid = [1e9] * len(edges_gdf)
    else:
        for edge_geometry in edges_gdf.geometry:
            min_distance_to_avoid.append(float(avoid_points_gdf.distance(edge_geometry).min()))

    edges_gdf["min_dist"] = min_distance_to_avoid

    # basis "kosten" = lengte van de weg (meters)
    edges_gdf["weight"] = edges_gdf["length"].astype(float)

    # als edge binnen radius valt, maak hem duurder
    within_avoid_zone = edges_gdf["min_dist"] <= float(avoid_radius_m)
    edges_gdf.loc[within_avoid_zone, "weight"] = (
        edges_gdf.loc[within_avoid_zone, "length"].astype(float) * float(penalty_multiplier)
    )

    # 5) Weight terug in de graaf zetten
    weighted_graph = projected_graph.copy()

    for (u, v, k), row in edges_gdf.iterrows():
        if weighted_graph.has_edge(u, v, k):
            weighted_graph[u][v][k]["weight"] = float(row["weight"])
            weighted_graph[u][v][k]["min_dist"] = float(row["min_dist"])

    # 6) Route berekenen (kortste pad op basis van weight)
    try:
        route_node_ids = nx.shortest_path(
            weighted_graph,
            start_node_id,
            end_node_id,
            weight="weight",
        )
    except nx.NetworkXNoPath:
        raise RuntimeError(
            "Geen route gevonden. Probeer avoid_radius_m kleiner of penalty_multiplier lager."
        )

    # 7) Route omzetten naar lat/lon lijst (voor kaart & export)
    route_latlon = []
    for node_id in route_node_ids:
        if node_id in wgs_graph.nodes:
            lat = wgs_graph.nodes[node_id]["y"]
            lon = wgs_graph.nodes[node_id]["x"]
            route_latlon.append((float(lat), float(lon)))

    # 8) Folium kaart maken en tekenen
    folium_map = folium.Map(location=start_latlon, zoom_start=14)

    # route lijn
    folium.PolyLine(
        route_latlon,
        weight=6,
        opacity=0.85,
        tooltip="Route (vermijdt avoid-zones)"
    ).add_to(folium_map)

    # start/eind markers
    folium.Marker(start_latlon, tooltip="Start").add_to(folium_map)
    folium.Marker(end_latlon, tooltip="Eind").add_to(folium_map)

    # avoid punten + cirkels
    for (lat, lon) in avoid_latlon_list:
        folium.Circle(
            location=(lat, lon),
            radius=float(avoid_radius_m),
            fill=True,
            fill_opacity=0.15,
            tooltip=f"Avoid-zone ({avoid_radius_m:.0f} m)"
        ).add_to(folium_map)

        folium.Marker((lat, lon), tooltip="Avoid punt").add_to(folium_map)

    # 9) Opslaan (HTML)
    html_path = Path(output_html).resolve()
    folium_map.save(str(html_path))

if __name__ == "__main__":
    app.run()