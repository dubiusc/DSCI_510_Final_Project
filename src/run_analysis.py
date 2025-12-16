import pandas as pd
import numpy as np


def run_analysis():

    # Loading raw dataset 
    city_env_df = pd.read_csv("../data/processed/city_environment_clean.csv")

    print(city_env_df.shape)
    print("\nColumn info:")
    print(city_env_df.info())

    print("\nFirst 5 rows:")
    print(city_env_df.head())

    #Computing AQI based on PM2.5 concentration.
    #Formula taken from US EPA

    aqi_calc = []

    for i, row in city_env_df.iterrows():
        pm25 = row["pm25"]

        if pd.isna(pm25):
            aqi_calc.append(None)

        elif 0.0 <= pm25 <= 12.0:
            aqi = ((50 - 0) / (12.0 - 0.0)) * (pm25 - 0.0) + 0
            aqi_calc.append(round(aqi))

        elif 12.1 <= pm25 <= 35.4:
            aqi = ((100 - 51) / (35.4 - 12.1)) * (pm25 - 12.1) + 51
            aqi_calc.append(round(aqi))

        elif 35.5 <= pm25 <= 55.4:
            aqi = ((150 - 101) / (55.4 - 35.5)) * (pm25 - 35.5) + 101
            aqi_calc.append(round(aqi))

        elif 55.5 <= pm25 <= 150.4:
            aqi = ((200 - 151) / (150.4 - 55.5)) * (pm25 - 55.5) + 151
            aqi_calc.append(round(aqi))

        elif 150.5 <= pm25 <= 250.4:
            aqi = ((300 - 201) / (250.4 - 150.5)) * (pm25 - 150.5) + 201
            aqi_calc.append(round(aqi))

        elif 250.5 <= pm25 <= 350.4:
            aqi = ((400 - 301) / (350.4 - 250.5)) * (pm25 - 250.5) + 301
            aqi_calc.append(round(aqi))

        elif 350.5 <= pm25 <= 500.4:
            aqi = ((500 - 401) / (500.4 - 350.5)) * (pm25 - 350.5) + 401
            aqi_calc.append(round(aqi))

        else:
            aqi_calc.append(None)

    city_env_df["aqi_pm25"] = aqi_calc

    print(city_env_df[["city", "pm25", "aqi_pm25"]].head(10))


    # Air quality severity distribution
    city_env_df["aqi_category"] = "-"

    city_env_df.loc[city_env_df["aqi_pm25"] <= 50, "aqi_category"] = "Good"
    city_env_df.loc[(city_env_df["aqi_pm25"] > 50) & (city_env_df["aqi_pm25"] <= 100), "aqi_category"] = "Moderate"
    city_env_df.loc[(city_env_df["aqi_pm25"] > 100) & (city_env_df["aqi_pm25"] <= 150), "aqi_category"] = "Sensitive(unhealthy)"
    city_env_df.loc[(city_env_df["aqi_pm25"] > 150) & (city_env_df["aqi_pm25"] <= 200), "aqi_category"] = "Unhealthy"
    city_env_df.loc[city_env_df["aqi_pm25"] > 200, "aqi_category"] = "Hazardous"

    print("\nAQI category counts:")
    print(city_env_df["aqi_category"].value_counts())

    # Population vs air quality 

    city_env_df["population_group"] = "Small"

    city_env_df.loc[city_env_df["population"] >= 1_000_000, "population_group"] = "Medium"
    city_env_df.loc[city_env_df["population"] >= 5_000_000, "population_group"] = "Large"
    city_env_df.loc[city_env_df["population"] >= 10_000_000, "population_group"] = "Mega"

    print("\nAverage AQI by population group:")
    print(
        city_env_df.groupby("population_group")["aqi_pm25"]
        .mean()
        .sort_values(ascending=False)
    )

    # Weather influence on air pollution

    print("\nCorrelation between weather variables and AQI:")
    print(city_env_df[["temperature", "windspeed", "aqi_pm25"]].corr())

    print("\nAverage AQI by temperature range:")
    city_env_df["temp_category"] = None

    for i, row in city_env_df.iterrows():
        temp = row["temperature"]

        if temp <= 10:
            city_env_df.loc[i, "temp_category"] = "Cold"
        elif temp <= 25:
            city_env_df.loc[i, "temp_category"] = "Moderate"
        else:
            city_env_df.loc[i, "temp_category"] = "Hot"

    mean_aqi_by_temp = (city_env_df.groupby("temp_category")["aqi_pm25"].mean())
    print(mean_aqi_by_temp)


    # Pollutant contribution to AQI

    print("\nCorrelation of pollutants with AQI:")
    pollution_corr = (
        city_env_df[["pm25", "pm10", "no2", "o3", "aqi_pm25"]]
        .corr()["aqi_pm25"]
        .sort_values(ascending=False)
    )
    print(pollution_corr)

    # Ranking cities by environmental stress

    print("\nTop 10 most polluted cities (by AQI):")
    print(
        city_env_df[["city", "country", "aqi_pm25"]]
        .sort_values("aqi_pm25", ascending=False)
        .head(10)
    )

    print("\nLeast polluted cities (by AQI):")
    print(
        city_env_df[["city", "country", "aqi_pm25"]]
        .sort_values("aqi_pm25")
        .head(10)
    )

    return city_env_df


if __name__ == "__main__":
    run_analysis()