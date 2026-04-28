from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# 🔑 Put your OpenWeather API key here
API_KEY = "cddbac2b6b6a4c1d301f284b0b71e7c8"

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    aqi = None

    # 📊 Handle form (prediction)
    if request.method == 'POST':
        try:
            pm25 = float(request.form['pm25'])
            pm10 = float(request.form['pm10'])

            # Simple formula (for demo)
            prediction = round((pm25 * 0.5 + pm10 * 0.5), 2)

        except:
            prediction = "Invalid input"

    # 🌍 Get real AQI data (example: Delhi)
    try:
        lat = 28.6139
        lon = 77.2090

        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        aqi = data['list'][0]['main']['aqi']
        components = data['list'][0]['components']

        # 📊 Create graph
        labels = list(components.keys())
        values = list(components.values())

        os.makedirs("static", exist_ok=True)

        plt.figure()
        plt.bar(labels, values)
        plt.title("Air Pollution Components")
        plt.xticks(rotation=45)

        graph_path = "static/graph.png"
        plt.savefig(graph_path)
        plt.close()

    except:
        aqi = "API Error"

    # 🔥 Send everything to HTML
    return render_template(
        'index.html',
        prediction=prediction,
        aqi=aqi,
        graph="graph.png"
    )

if __name__ == "__main__":
    app.run(debug=True)