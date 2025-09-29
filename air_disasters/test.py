import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def extract_fatalities_and_occupants(df):
    """
    Parses the 'passengers' column into 'Fatalities' and 'Occupants' columns.
    Adds a 'FatalityRate' column.

    Example code: df = extract_fatalities_and_occupants(df)
    """

    df[["Fatalities", "Occupants"]] = df["passengers"].apply(lambda x: pd.Series(extract_numbers(str(x)))) #Incredible amount of formatting
    df = df.dropna(subset=["Fatalities", "Occupants"]) # Drop any that don't have our required data
    df["FatalityRate"] = df["Fatalities"] / df["Occupants"].replace(0, pd.NA) # readds NONE, to make it easier to work with
    df["airline"] = df["airline"].astype(str).str.strip()
    return df


def extract_numbers(cell):
    """
    Tries to get the numbers out of a badly formatted column. Works by splitting occupants from fatalities, then the string from the number.

    Example code: extract_numbers(x)
    """
    try: # Not clean code. Hides bugs. But not all cells will have the data we want, and this is the best way to handle all the failures.
        fatalities = int(cell.split("/")[0].split(":")[1].strip())
        occupants = int(cell.split("/")[1].split(":")[1].strip())
        return fatalities, occupants
    except:
        return None, None


def airline_statistics(df, number):
    """
    Aggregates total crashes and average fatality rate per airline.
    Returns the top_n airlines by number of crashes.

    Example code: stats = airline_statistics(df, 10)
    """
    return ( # Turns out, you can use () to get multiple functions stacked on top of eachother. Who knew?
        df.groupby("airline") 
        .agg(
            crashes=("airline", "count"),
            avg_fatality_rate=("FatalityRate", "mean")
        )
        .sort_values("crashes", ascending=False)
        .head(number)
    )


def plot_crashes_vs_fatality_rate(df):
    """
    Plots a combined bar (total crashes) and line (fatality rate) chart.

    Example code:
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(df.index, df["crashes"], color="skyblue", label="Total Crashes")
    ax1.set_ylabel("Total Crashes")
    ax1.set_xlabel("Airline")
    ax1.tick_params(axis="x", rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(
        df.index,
        df["avg_fatality_rate"] * 100, # We want percentages
        color="red", #Red is nice.
        marker="o", #Mark each datapoint
        linewidth=2,
        label="Avg Fatality Rate (%)",
    )
    ax2.set_ylabel("Average Fatality Rate (%)")

    fig.suptitle("Top Airlines: Crashes vs Fatality Rate", fontsize=14)
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.tight_layout()
    plt.show()


def plot_age_vs_fatality_rate(df):
    """
    Plots Aircraft Age vs Fatality Rate, summarized by Aircraft Type categories,
    with a trend line showing overall relationship.

    Example code:
    """

    df["accident_date"] = pd.to_datetime(df["accident_date"], errors="coerce")
    df["first_flight"] = pd.to_datetime(df["first_flight"].str.split(" ").str[0], errors="coerce")

    df["AircraftAge"] = (df["accident_date"] - df["first_flight"]).dt.days / 365.25 #convert to days (365.25 days in a year)

    clean_df = df.dropna(subset=["AircraftAge", "FatalityRate", "airplane_type"]).copy()

    def categorize_type(x: str) -> str:
        x = str(x).lower()
        if "airbus" in x:
            return "Airbus"
        elif "boeing" in x:
            return "Boeing"
        elif "cessna" in x:
            return "Cessna"
        elif "embraer" in x:
            return "Embraer"
        elif "bombardier" in x or "canadair" in x:
            return "Bombardier"
        elif "antonov" in x or "tupolev" in x or "ilyushin" in x:
            return "Soviet/Russian"
        else:
            return "Other/Unknown"

    clean_df["TypeCategory"] = clean_df["airplane_type"].apply(categorize_type)

    plt.figure(figsize=(12, 6))
    for category, group in clean_df.groupby("TypeCategory"):
        plt.scatter(
            group["AircraftAge"],
            group["FatalityRate"] * 100,
            label=category,
            alpha=0.6
        )

    x = pd.to_numeric(clean_df["AircraftAge"], errors="coerce")
    y = pd.to_numeric(clean_df["FatalityRate"] * 100, errors="coerce")
    mask = x.notna() & y.notna()
    x_clean = x[mask]
    y_clean = y[mask]

    if len(x_clean) > 1:  # Only fit if enough points
        coeffs = np.polyfit(x_clean, y_clean, 1)  # linear fit
        poly = np.poly1d(coeffs)
        xs = np.linspace(x_clean.min(), x_clean.max(), 200)
        plt.plot(xs, poly(xs), color="black", linewidth=2, linestyle="--", label="Trend Line")

    plt.title("Aircraft Age vs Fatality Rate by Aircraft Type")
    plt.xlabel("Aircraft Age (years)")
    plt.ylabel("Fatality Rate (%)")
    plt.gca().invert_xaxis()
    plt.legend(title="Aircraft Type Category", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()



data_location = "air_disasters/data/airdisaster(in).csv"

df = pd.read_csv(data_location, sep=";", encoding="ISO-8859-1", skiprows=1, on_bad_lines="skip")
df = extract_fatalities_and_occupants(df)
stats = airline_statistics(df, 10)
plot_crashes_vs_fatality_rate(stats)
plot_age_vs_fatality_rate(df)
