import pandas as pd
import random


data_location = "python\workshop\Data Scheet Movies 1.csv"
df = pd.read_csv(data_location, sep=";")

for index, row in df.iterrows():
    print(f"{index}: {row}")


choice = random.randint(0, len(df) - 1)
print(df.loc[choice])