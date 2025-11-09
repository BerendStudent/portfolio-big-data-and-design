import requests

# Requests water surface temperature at a given location; currently set to "Nieuwegein Lekkanaal", because it is the closest location to me that works.

link = "https://waterwebservices.beta.rijkswaterstaat.nl/test/ONLINEWAARNEMINGENSERVICES/OphalenLaatsteWaarnemingen"
location = "nieuwegein.lekkanaal"

payload = {
    "LocatieLijst": [{"Code": location}],
    "AquoPlusWaarnemingMetadataLijst": [{
        "AquoMetadata": {
            "Compartiment": {"Code": "OW"},
            "Grootheid": {"Code": "T"}
        }
    }]
}

response = requests.post(link, json=payload)
try:
    print(response.json()["WaarnemingenLijst"][0]["MetingenLijst"][0]["Meetwaarde"]["Waarde_Numeriek"])
except:
    print(response)

def get_temp():
    link = "https://waterwebservices.beta.rijkswaterstaat.nl/test/ONLINEWAARNEMINGENSERVICES/OphalenLaatsteWaarnemingen"
    location = "nieuwegein.lekkanaal"

    payload = {
        "LocatieLijst": [{"Code": location}],
        "AquoPlusWaarnemingMetadataLijst": [{
            "AquoMetadata": {
                "Compartiment": {"Code": "OW"},
                "Grootheid": {"Code": "T"}
            }
        }]
    }

    response = requests.post(link, json=payload)
    try:
        print(response.json()["WaarnemingenLijst"][0]["MetingenLijst"][0]["Meetwaarde"]["Waarde_Numeriek"])
    except:
        print("Temp error response:", response)