import folium


mapObj = folium.Map(
    location=[50, 10],
    zoom_start=5
)

markerObj = folium.Marker(
    location=[52.088250, 5.130870],
    popup="<b>ENG PERSOON</b>"
)

secondMarkerObj = folium.Marker(
    location=[52.088230, 5.130880],
    popup="GROTE WOLF"
)

markerObj.add_to(mapObj)
secondMarkerObj.add_to(mapObj)

mapObj.save("startup/app/templates/berlin_map.html")
