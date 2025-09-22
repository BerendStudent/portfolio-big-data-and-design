import pandas as pd

data_location = "design\data story\Vermeden_verbruik_fossiele_energie_en_emissie_CO2_22092025_034643.csv"
df = pd.read_csv(data_location, sep=";", quotechar='"', skiprows=3)

print(df.loc[0])
print(df.info)