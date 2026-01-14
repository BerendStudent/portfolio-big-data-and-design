from flask import Flask, request, render_template, redirect
import pandas as pd
import folium
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
import uuid
import threading

app = Flask(__name__)

CSV_PATH = "startup/app/points.csv"
STATIC_MAP_PATH = "startup/app/static/berlin_map.html"
STATIC_ROUTE_PATH = "startup/app/static/route.html"
route_jobs = {}


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
        folium.Marker(
            location=[point.lat, point.lon],
            popup=f"<b>{point.description}</b>"
        ).add_to(mapObj)

    mapObj.save(STATIC_MAP_PATH)
    return ("", 204)


def create_safe_route_map(
    city_query,
    travel_mode,
    start_latlon,
    end_latlon,
    avoid_radius_m,
    penalty_multiplier,
    output_html,
):
    ox.settings.use_cache = True
    ox.settings.log_console = False

    df = pd.read_csv(CSV_PATH)
    avoid_latlon_list = list(zip(df["lat"], df["lon"]))

    projected_graph = ox.graph_from_place(city_query, network_type=travel_mode)
    projected_graph = ox.project_graph(projected_graph)

    wgs_graph = ox.graph_from_place(city_query, network_type=travel_mode)

    start_node_id = ox.distance.nearest_nodes(
        wgs_graph, X=start_latlon[1], Y=start_latlon[0]
    )
    end_node_id = ox.distance.nearest_nodes(
        wgs_graph, X=end_latlon[1], Y=end_latlon[0]
    )

    nodes_gdf = ox.graph_to_gdfs(projected_graph, nodes=True, edges=False)

    avoid_points_gdf = gpd.GeoDataFrame(
        df.assign(id=range(len(df))),
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs="EPSG:4326",
    ).to_crs(nodes_gdf.crs)

    edges_gdf = ox.graph_to_gdfs(projected_graph, nodes=False, edges=True).copy()

    if len(avoid_points_gdf) == 0:
        edges_gdf["min_dist"] = 1e9
    else:
        edges_gdf["min_dist"] = [
            float(avoid_points_gdf.distance(geom).min())
            for geom in edges_gdf.geometry
        ]

    edges_gdf["weight"] = edges_gdf["length"].astype(float)
    within = edges_gdf["min_dist"] <= float(avoid_radius_m)
    edges_gdf.loc[within, "weight"] *= float(penalty_multiplier)

    weighted_graph = projected_graph.copy()
    for (u, v, k), row in edges_gdf.iterrows():
        weighted_graph[u][v][k]["weight"] = float(row["weight"])

    route_node_ids = nx.shortest_path(
        weighted_graph,
        start_node_id,
        end_node_id,
        weight="weight",
    )

    route_latlon = [
        (wgs_graph.nodes[n]["y"], wgs_graph.nodes[n]["x"])
        for n in route_node_ids
        if n in wgs_graph.nodes
    ]

    folium_map = folium.Map(location=start_latlon, zoom_start=14)

    folium.PolyLine(route_latlon, weight=6, opacity=0.85).add_to(folium_map)
    folium.Marker(start_latlon, tooltip="Start").add_to(folium_map)
    folium.Marker(end_latlon, tooltip="End").add_to(folium_map)

    for lat, lon in avoid_latlon_list:
        folium.Circle(
            location=(lat, lon),
            radius=float(avoid_radius_m),
            fill=True,
            fill_opacity=0.15,
        ).add_to(folium_map)

    folium_map.save(output_html)

def route_worker(job_id, params):
    try:
        route_jobs[job_id]["status"] = "running"

        create_safe_route_map(**params)

        route_jobs[job_id]["status"] = "done"
    except Exception as e:
        route_jobs[job_id]["status"] = "error"
        route_jobs[job_id]["error"] = str(e)


@app.route("/start_route", methods=["POST"])
def start_route():
    data = request.json

    job_id = str(uuid.uuid4())
    route_jobs[job_id] = {"status": "queued", "error": None}

    params = {
        "city_query": data["city_query"],
        "travel_mode": data["travel_mode"],
        "start_latlon": tuple(data["start_latlon"]),
        "end_latlon": tuple(data["end_latlon"]),
        "avoid_radius_m": float(data["avoid_radius_m"]),
        "penalty_multiplier": float(data["penalty_multiplier"]),
        "output_html": STATIC_ROUTE_PATH,
    }

    threading.Thread(
        target=route_worker,
        args=(job_id, params),
        daemon=True,
    ).start()

    return {"job_id": job_id}, 202


@app.route("/route_status/<job_id>")
def route_status(job_id):
    job = route_jobs.get(job_id)
    if not job:
        return {"error": "Unknown job"}, 404
    return job


if __name__ == "__main__":
    app.run(debug=True)
