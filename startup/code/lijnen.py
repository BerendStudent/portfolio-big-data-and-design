import pandas as pd


data_location = "startup\data\haltesutrecht.csv"
df = pd.read_csv(data_location)

print(df.loc[0])