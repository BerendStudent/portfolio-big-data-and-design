import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd

CSV_PATH = "startup/app/points.csv"

mapObj = folium.Map(
    location=[52.081730, 5.104691],
    zoom_start=15
)

df = pd.read_csv(CSV_PATH)

avoid_points = list(zip(df["lat"], df["lon"], df["description"]))

data = []

for lat, lon, _, in avoid_points:
    data.append([lat, lon, 1])

HeatMap(data).add_to(mapObj)


mapObj.save("startup/app/static/heatmap.html")
