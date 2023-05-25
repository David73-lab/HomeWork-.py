
# თავიდან 16 დღიანიამინდის პროგნოზის დაწერა მინდოდა მაგრამ არ იმუშავა პროგრამამ
# import requests
# api_key = "ad54c1689a6fa5a910ee976ff1e759b2"
# base_url = "https://api.openweathermap.org/data/2.5/forecast/daily"
# city = "Tbilisi"
# num_days = 16
#
# complete_url = f"{base_url}?q={city}&cnt={num_days}&appid={api_key}"
#
# response = requests.get(complete_url)
#
# if response.status_code == 200:
#     print("Status code:", response.status_code)
#     print("Headers:", response.headers)
#
#
#     weather_data = response.json()
#
#     for i in range(num_days):
#         date = weather_data["list"][i]["dt"]
#         temp = weather_data["list"][i]["temp"]["day"]
#         print("Date:", date, "Temp:", temp)
# else:
#     print("Error:", response.status_code)
# /////////////////////////////////////////////////////////////////

import requests
import json
import sqlite3


api_key = "ad54c1689a6fa5a910ee976ff1e759b2"
base_url = "https://api.openweathermap.org/data/2.5/forecast"

# citi
city = "Tbilisi"


complete_url = f"{base_url}?q={city}&appid={api_key}"

response = requests.get(complete_url)

if response.status_code == 200:
    print("Status code:", response.status_code)
    print("Headers:", response.headers)

    weather_data = response.json()


    with open("weather_forecast.json", "w") as json_file:
        json.dump(weather_data, json_file)


    conn = sqlite3.connect("weather_database.db")
    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS weather (
                    date_time TEXT,
                    temperature FLOAT,
                    humidity INTEGER,
                    weather_description TEXT
                )''')



    hourly_forecast = weather_data["list"]
    for forecast in hourly_forecast:
        date_time = forecast["dt_txt"]
        temperature = forecast["main"]["temp"]
        humidity = forecast["main"]["humidity"]
        weather_description = forecast["weather"][0]["description"]

        c.execute('''INSERT INTO weather (date_time, temperature, humidity, weather_description)
                        VALUES (?, ?, ?, ?)''', (date_time, temperature, humidity, weather_description))


    conn.commit()
    conn.close()

    print("Weather data saved to JSON file and database.")
else:
    print("Error:", response.status_code)




