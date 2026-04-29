from flask import Flask, render_template, request
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

API_KEY = "cddbac2b6b6a4c1d301f284b0b71e7c8"

# 🔹 AQI category + health advice
def get_aqi_info(aqi):
    data = {
        1: ("Good", "Air quality is good 😊", "green"),
        2: ("Fair", "Air is acceptable 🙂", "lightgreen"),
        3: ("Moderate", "Limit outdoor activity ⚠️", "orange"),
        4: ("Poor", "Wear mask 😷", "red"),
        5: ("Very Poor", "Stay indoors 🚫", "purple")
    }
    return data.get(aqi, ("Unknown", "No data", "black"))

# 🔹 Get coordinates from city
def get_coordinates(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url).json()

    # 🔥 FIX: check if response is empty or invalid
    if not response or not isinstance(response, list):
        return None, None

    return response[0]['lat'], response[0]['lon']

# 🔹 Get AQI data
def get_aqi_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url).json()

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    aqi_text = None
    advice = None
    color = "black"
    graph = None

    if request.method == 'POST':
        city = request.form.get('city')

        # 🔸 Prediction (simple logic)
        try:
            pm25 = float(request.form.get('pm25', 0))
            pm10 = float(request.form.get('pm10', 0))
            prediction = f"Predicted AQI: {round((pm25 + pm10)/2, 2)}"
        except:
            prediction = "Invalid input"

        # 🔸 Get coordinates
        lat, lon = get_coordinates(city)
        if lat is None or lon is None:
            aqi_text = "❌ City not found or API error"
            return render_template(
                'index.html',
                prediction=prediction,
                aqi_text=aqi_text,
                color="red",
                graph=None
    )

        if lat is None:
            aqi_text = "City not found"
        else:
            data = get_aqi_data(lat, lon)

            try:
                aqi = data['list'][0]['main']['aqi']
                components = data['list'][0]['components']
                labels = list(components.keys())
                values = list(components.values())

                category, advice, color = get_aqi_info(aqi)
                aqi_text = f"{city}: AQI {aqi} ({category})"

                # 🔸 Create graph using pandas
                df = pd.DataFrame(list(components.items()), columns=['Pollutant', 'Value'])

                os.makedirs("static", exist_ok=True)

                plt.figure()
                plt.bar(df['Pollutant'], df['Value'])
                plt.xticks(rotation=45)
                plt.title(f"Pollution Levels in {city}")
                plt.tight_layout()

                
                plt.close()

                graph = "graph.png"

            except:
                aqi_text = "Error fetching AQI data"

    return render_template(
    'index.html',
    prediction=prediction,
    aqi_text=aqi_text,
    color=color,
    labels=labels,
    values=values
)

if __name__ == "__main__":
    app.run(debug=True)