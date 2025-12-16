import requests
import pandas as pd
import time
from bs4 import BeautifulSoup


def get_cities():
    """
    The function extracts city names, corresponding countries, and population 
    values from a public HTML table. 

    Returns:
    DataFrame:
    A DataFrame containing raw city data with columns representing
    city name, country, and population (as strings).

    
    """
    url = "https://worldpopulationreview.com/cities"
    headers = {"User-Agent": "Mozilla/5.0"} #To avoid banning of automated requests by the website, HTTP requests contains a User-Agent header that mimicks a real browser.

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")

    cities = []

    for row in rows:
        rows_html = row.find_all("td")
        try:
            city = rows_html[2].get_text(strip=True)
            country = rows_html[3].get_text(strip=True)
            pop_text = rows_html[4].get_text(strip=True).replace(",", "")
            cities.append([city, country, pop_text])
        except IndexError:
            continue

    return pd.DataFrame(cities)



def get_lat_lon(city, country):
    """
    Returns latitude and longitude for a given city and country using the Nominatim API
    which is a geocoding website that gives the coordinates of a place based on its name.

    Parameters:
    city:(str): Name of the city
    country (str): Name of the country

    Returns:
    tuple: (latitude, longitude)
    Returns (None, None) if the location is not found or an error occurs.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"city": city, "country": country, "format": "json"}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10).json()
        if response:
            return float(response[0]["lat"]), float(response[0]["lon"])
    except:
        pass

    return None, None


def get_weather(lat, lon):
    """
    Returns the current temperature, wind direction, and wind speed for a 
    specified latitude and longitude for a city which are generated 
    by the get_lan_lon() function.

    Parameters:
    lat (float): Latitude of the location
    lon (float): Longitude of the location

    Retruns:
    tuple: (temperature, windspeed, winddirection)
    Returns None for values if data is unavailable or an error occurs.
    """
    url = ("https://api.open-meteo.com/v1/forecast?")

    params = {"latitude": lat, "longitude": lon, "current_weather": True}


    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        weather = data["current_weather"]
        temperature = weather["temperature"]
        windspeed = weather["windspeed"]
        winddirection = weather["winddirection"]

        return temperature, windspeed, winddirection
    except:
        return None, None, None


def get_air_quality(lat, lon):
    """
    retrieves current PM2.5, PM10, nitrogen dioxide (NO2), and ozone (O3) values 
    based on latitude and longitude using the Open-Meteo Air Quality API.
    
    Parameters:
    lat (float): Latitude of the location
    lon (float): Longitude of the location

    Returns:
    tuple: (pm25, pm10, no2, o3)
    Returns None for values if data is unavailable or an error occurs.
    """
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {"latitude": lat, "longitude": lon, "current": "pm2_5,pm10,nitrogen_dioxide,ozone"}

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        air = data["current"]
        pm25 = air.get("pm2_5")
        pm10 = air.get("pm10")
        no2 = air.get("nitrogen_dioxide")
        o3 = air.get("ozone")

        return pm25, pm10, no2, o3
    except:
        return None, None, None, None


def create_dataset():
    """
    The function scrapes city names, countries, and population values 
    by calling get_cities(), retrieves latitude and longitude for each city 
    by calling get_lat_lon(), and fetches current weather and air quality 
    information using APIs by calling get_weather() and get_air_quality() 
    and stores them as a pandas dataframe.

    Returns:
    pandas.DataFrame containing raw city level environmental data.
    """
    cities_data = get_cities()
    rows = []

    for i, row in cities_data.iterrows():
        city, country, population = row

        #print(f"{i+1}/{len(cities_data)}  Processing: {city}, {country}")

        lat, lon = get_lat_lon(city, country)
        time.sleep(1)
 
        try:
            temperature, windspeed, winddirection = get_weather(lat, lon)
            pm25, pm10, no2, o3 = get_air_quality(lat, lon)
        except:
            continue

        rows.append([city, country, population,lat, lon, temperature, windspeed, winddirection, pm25, pm10, no2, o3])

        time.sleep(0.2)

    complete_dataset = pd.DataFrame(rows)

    complete_dataset.to_csv("data/raw/city_environment_raw.csv", index=False, header=False)
    print("Shape", complete_dataset.shape)

    return complete_dataset

if __name__ == "__main__":
    create_dataset()
