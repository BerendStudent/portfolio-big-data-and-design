import pandas as pd


data_location = "air_disasters/data/airdisaster(in).csv"
df = pd.read_csv(data_location, sep=";", encoding="ISO-8859-1", skiprows=1, on_bad_lines='skip')

airlines_dict = {}

for index, row in df.iterrows():
    crash = row.to_dict() 
    airline = crash['airline']
    if airline in airlines_dict:
        airlines_dict[airline] += 1
    else:
        airlines_dict[airline] = 1
    
sorted_dict = dict(sorted(airlines_dict.items(), key=lambda item: item[1], reverse=True))
for i in range(0, 10):
    top_crasher = list(sorted_dict)[i]
    print(top_crasher)
    print(sorted_dict[top_crasher])

