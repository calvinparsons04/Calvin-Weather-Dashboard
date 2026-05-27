
import requests
import pandas as pd
from datetime import datetime
import os

API_KEY = "rv6nbvyvth0ug8mxupupp8iqcihtbgbc"
API_SECRET = "s7sjjsut3vfduyv9qnjlvbqllmlvvkkv"
STATION_ID = 175546

headers = {"X-Api-Secret": API_SECRET}


try:

    url = f"https://api.weatherlink.com/v2/current/{STATION_ID}?api-key={API_KEY}"

    esponse = requests.get(url, headers=headers, timeout=10)

    data = response.json()

    all_data = {}

    for sensor in data["sensors"]:
        for reading in sensor["data"]:
            all_data.update(reading)

        weather_data = {
            "Time": datetime.now(),

            "Temperature": all_data.get("temp"),
            "Feels Like": all_data.get("thw_index") or all_data.get("heat_index") or all_data.get("wind_chill"),
            "Humidity": all_data.get("hum"),

            "Pressure": all_data.get("bar_sea_level"),
            "Pressure Trend": all_data.get("bar_trend"),

            "Rain Today": all_data.get("rainfall_day_in"),
            "Rain Rate": all_data.get("rain_rate_last_in") or 0,
            "Rain Last 24 Hr": all_data.get("rainfall_last_24_hr_in"),

            "Wind Speed": all_data.get("wind_speed_avg_last_1_min"),
          
            "Wind Gust": all_data.get("wind_speed_avg_last_1_min") or 0,
    
            "Wind Direction": all_data.get("wind_dir_scalar_avg_last_1_min"),
            "Dew Point": all_data.get("dew_point"),
        }

        df = pd.DataFrame([weather_data])

        file_exists = os.path.exists("weather_data_big.csv")

        df.to_csv(
            "weather_data_big.csv",
            mode="a",
            header=not file_exists,
            index=False
        )

        print("Saved:", datetime.now())

    except Exception as e:
        print("ERROR:", e)
