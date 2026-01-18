import requests

params = {
    'kenteken': 'J390RH'
}

response = requests.get('https://opendata.rdw.nl/resource/m9d7-ebf2.json',params=params).json()

if response:
    print(response[0].get('handelsbenaming', 'Unknown'))
else:
    print('Kenteken not found')
