from flask import Flask, request, render_template, redirect, url_for, make_response
import pandas as pd
from markupsafe import escape
import folium

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
        location=[50, 10],
        zoom_start=5
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

if __name__ == "__main__":
    app.run()