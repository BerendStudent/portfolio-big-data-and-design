from flask import Flask, request, render_template, jsonify
import pandas as pd
import folium
import osmnx as ox
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import uuid

app = Flask(__name__)

CSV_PATH = "startup/app/points.csv"
STATIC_DIR = "startup/app/static"

executor = ThreadPoolExecutor(max_workers=2)
route_jobs: dict[str, dict] = {}


def getPoints():
    return pd.read_csv(CSV_PATH)


def placePoint(lat, lon, description):
    df = pd.read_csv(CSV_PATH)
    df.loc[len(df)] = [lat, lon, description]
    df.to_csv(CSV_PATH, index=False)


@lru_cache(maxsize=1000)
def geocode_address(address: str) -> tuple[float, float]:
    lat, lon = ox.geocode(address)
    return float(lat), float(lon)


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
    return ("", 204)


@app.route("/reset_map", methods=["POST"])
def reset_map():
    fmap = folium.Map(location=[52.081730, 5.104691], zoom_start=10)

    for p in getPoints().itertuples(index=False):
        folium.Marker(
            [p.lat, p.lon],
            popup=f"<b>{p.description}</b>",
            icon=folium.Icon(color="red", icon="exclamation-sign"),
            tooltip=p.description
        ).add_to(fmap)

    fmap.save(f"{STATIC_DIR}/berlin_map.html")
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
    avoid_points = list(zip(df["lat"], df["lon"], df["description"]))


    G_wgs = ox.graph_from_place(city_query, network_type=travel_mode)
    G_proj = ox.project_graph(G_wgs)


    start_node = ox.distance.nearest_nodes(G_wgs, start_latlon[1], start_latlon[0])
    end_node = ox.distance.nearest_nodes(G_wgs, end_latlon[1], end_latlon[0])


    nodes_gdf = ox.graph_to_gdfs(G_proj, nodes=True, edges=False)

    avoid_gdf = gpd.GeoDataFrame(
        df[["lat", "lon", "description"]],
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs="EPSG:4326"
    ).to_crs(nodes_gdf.crs)


    edges_gdf = ox.graph_to_gdfs(G_proj, nodes=False, edges=True).copy()

    if len(avoid_gdf) > 0:
        edges_gdf["min_dist"] = edges_gdf.geometry.apply(
            lambda g: avoid_gdf.distance(g).min()
        )
    else:
        edges_gdf["min_dist"] = 1e9

    edges_gdf["weight"] = edges_gdf["length"]
    edges_gdf.loc[
        edges_gdf["min_dist"] <= avoid_radius_m, "weight"
    ] *= penalty_multiplier

    for (u, v, k), row in edges_gdf.iterrows():
        G_proj[u][v][k]["weight"] = float(row["weight"])


    route = nx.shortest_path(G_proj, start_node, end_node, weight="weight")
    coords = [(G_wgs.nodes[n]["y"], G_wgs.nodes[n]["x"]) for n in route]

    fmap = folium.Map(location=start_latlon, zoom_start=13)

    folium.PolyLine(
        coords,
        weight=6,
        color="#007bff",
        opacity=0.9,
        tooltip="Safe route"
    ).add_to(fmap)


    folium.Marker(start_latlon, tooltip="Start").add_to(fmap)
    folium.Marker(end_latlon, tooltip="End").add_to(fmap)

    for lat, lon, desc in avoid_points:
        folium.Circle(
            location=(lat, lon),
            radius=float(avoid_radius_m),
            color="red",
            fill=True,
            fill_opacity=0.15,
            weight=2,
            tooltip="Avoid zone"
        ).add_to(fmap)

        folium.Marker(
            location=(lat, lon),
            icon=folium.Icon(color="red", icon="exclamation-sign"),
            popup=f"<b>{desc}</b>",
            tooltip=desc
        ).add_to(fmap)


    fmap.save(output_html)


@app.route("/start_route", methods=["POST"])
def start_route():
    data = request.json
    job_id = str(uuid.uuid4())
    route_jobs[job_id] = {"status": "running"}

    try:
        start = (
            geocode_address(data["start_address"])
            if "start_address" in data
            else tuple(data["start_latlon"])
        )
        end = (
            geocode_address(data["end_address"])
            if "end_address" in data
            else tuple(data["end_latlon"])
        )
    except Exception as e:
        route_jobs[job_id] = {"status": "error", "error": str(e)}
        return jsonify(job_id=job_id)

    def task():
        try:
            create_safe_route_map(
                city_query=data["city_query"],
                travel_mode=data["travel_mode"],
                start_latlon=start,
                end_latlon=end,
                avoid_radius_m=float(data["avoid_radius_m"]),
                penalty_multiplier=float(data["penalty_multiplier"]),
                output_html=f"{STATIC_DIR}/route.html",
            )
            route_jobs[job_id]["status"] = "done"
        except Exception as e:
            route_jobs[job_id] = {"status": "error", "error": str(e)}

    executor.submit(task)
    return jsonify(job_id=job_id)


@app.route("/route_status/<job_id>")
def route_status(job_id):
    return jsonify(route_jobs.get(job_id, {"status": "unknown"}))


if __name__ == "__main__":
    app.run(debug=True)
