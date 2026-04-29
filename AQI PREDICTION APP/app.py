from flask import Flask, render_template, request
import requests
from datetime import datetime
time_now = datetime.now().strftime("%d %b %Y, %H:%M")
app = Flask(__name__)   

API_KEY = "cddbac2b6b6a4c1d301f284b0b71e7c8"


def get_coordinates(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url).json()

    if not response:
        return None, None

    return response[0]['lat'], response[0]['lon']


def get_aqi_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url).json()

def get_aqi_info(aqi):
    data = {
        1: ("Good", "Air quality is good", "green"),
        2: ("Fair", "Air is acceptable", "lightgreen"),
        3: ("Moderate", "Limit outdoor activity", "orange"),
        4: ("Poor", "Wear mask", "red"),
        5: ("Very Poor", "Stay indoors", "purple")
    }
    return data.get(aqi, ("Unknown", "No data", "black"))

@app.route('/', methods=['GET', 'POST'])
def home():
    aqi_text = None
    color = "black"
    labels = []
    values = []
    time = time_now

    if request.method == 'POST':
        city = request.form.get('city')
        pm25 = request.form.get('pm25')
        pm10 = request.form.get('pm10')

        if pm25 and pm10:
            try:
               pm25 = float(pm25)
               pm10 = float(pm10)
               prediction = f"Predicted AQI: {round((pm25 + pm10)/2, 2)}"
            except:
                  prediction = "Invalid input"
        else:
            prediction = None
    


        lat, lon = get_coordinates(city)   

        if lat is None:
            aqi_text = "City not found"
        else:
            data = get_aqi_data(lat, lon)
            aqi = data['list'][0]['main']['aqi']
            category, advice, color = get_aqi_info(aqi)
            aqi_text = f"{city}: AQI {aqi} ({category})"
            components = data['list'][0]['components']
            labels = list(components.keys())
            values = list(components.values())

    return render_template('index.html', aqi_text=aqi_text,color="white",labels=labels, values=values,time=time_now)



if __name__ == "__main__":
    app.run(debug=True)