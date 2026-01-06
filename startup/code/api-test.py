import http.client

conn = http.client.HTTPSConnection("p2000.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "8f331bb28amsh115581951278579p1dc551jsn3cdf9475058f",
    'x-rapidapi-host': "p2000.p.rapidapi.com"
}

conn.request("GET", "/latest?limit=10&flex=true", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))