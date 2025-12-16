import pandas as pd


def clean_dataset():
    """ Used for cleaning and preprocessing the raw dataset by handling
    missing values, converting numeric columns, removing duplicates, and sorting
    by population.

    Input: raw CSV file 
    Output: cleaned CSV file and a pandas DataFrame containing the cleaned data """

    df = pd.read_csv("../data/raw/city_environment_raw.csv", header=None)

    df.columns = [
        "city",
        "country",
        "population",
        "lat",
        "lon",
        "temperature",
        "windspeed",
        "winddirection",
        "pm25",
        "pm10",
        "no2",
        "o3"
    ]

    df = df.dropna(subset=["city", "country", "population"])

    numeric_cols = [
        "population",
        "lat",
        "lon",
        "temperature",
        "windspeed",
        "winddirection",
        "pm25",
        "pm10",
        "no2",
        "o3"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["population", "lat", "lon", "temperature", "pm25"])

    df = df.drop_duplicates(subset=["city", "country"])

    df = df.sort_values("population", ascending=False)

    df = df.reset_index(drop=True)

    df.to_csv("data/processed/city_environment_clean.csv", index=False)

    print("Saved : data/processed/city_environment_clean.csv")
    print("Final shape:", df.shape)

    return df

if __name__ == "__main__":
   df_clean = clean_dataset()