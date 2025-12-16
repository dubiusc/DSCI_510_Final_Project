import matplotlib.pyplot as plt
import numpy as np
from run_analysis import run_analysis

city_env_df = run_analysis()


corr_vars = city_env_df[
    ["aqi_pm25", "pm25", "pm10", "no2", "o3", "temperature", "windspeed"]
].corr()

#Which variables are most related to AQI overall?
plt.figure(figsize=(8, 6))
plt.imshow(corr_vars, cmap="coolwarm")
plt.colorbar(label="Correlation")

plt.xticks(range(len(corr_vars.columns)), corr_vars.columns, rotation=45)
plt.yticks(range(len(corr_vars.columns)), corr_vars.columns)

plt.title("Correlation Heatmap of AQI, Pollutants, and Weather Variables")
plt.tight_layout()
plt.show()

#How does AQI differ across city sizes beyond just averages?
plt.figure()
city_env_df.boxplot(
    column="aqi_pm25",
    by="population_group",
    grid=False
)
plt.title("AQI Distribution by City Population Group")
plt.suptitle("")
plt.xlabel("Population Group")
plt.ylabel("AQI")
plt.show()

#Does temperature meaningfully structure AQI values?
plt.figure()

for category in ["Cold", "Moderate", "Hot"]:
    subset = city_env_df[city_env_df["temp_category"] == category]
    plt.scatter(
        [category] * len(subset),
        subset["aqi_pm25"],
        alpha=0.4
    )

plt.title("AQI Distribution Across Temperature Categories")
plt.xlabel("Temperature Category")
plt.ylabel("AQI")
plt.show()

#Why does PM2.5 dominate AQI so strongly?
plt.figure()
plt.scatter(
    city_env_df["pm25"],
    city_env_df["aqi_pm25"],
    alpha=0.6
)
plt.title("PM2.5 vs AQI (EPA-Based Relationship)")
plt.xlabel("PM2.5 Concentration")
plt.ylabel("AQI")
plt.show()

#Are extreme AQI values concentrated in certain conditions?
high_aqi = city_env_df[city_env_df["aqi_pm25"] >= city_env_df["aqi_pm25"].quantile(0.75)]

plt.figure()
plt.scatter(
    high_aqi["temperature"],
    high_aqi["aqi_pm25"],
    alpha=0.6
)
plt.title("High AQI Values (Top 25%) vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("AQI")
plt.show()

#Which cities are most polluted?
top_polluted = (
    city_env_df[["city", "country", "aqi_pm25"]].sort_values("aqi_pm25", ascending=False).head(10))

labels = top_polluted["city"] + ", " + top_polluted["country"]

plt.figure(figsize=(8, 5))
plt.barh(labels, top_polluted["aqi_pm25"])
plt.xlabel("AQI")
plt.ylabel("City")
plt.title("Top 10 Most Polluted Cities (PM2.5-Based AQI)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()