from flask import Flask, jsonify, request, send_file
import requests
import os
from dotenv import load_dotenv

# Load environment variables from api.env
load_dotenv("api.env")
API_KEY = os.getenv("API_KEY")  # Fetch API_KEY from the environment

if not API_KEY:
    raise Exception("API_KEY is not set. Please check your api.env file.")

# Base URL for OpenWeatherMap API
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data
def get_weather(city_name):
    try:
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for HTTP failures
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Failed to connect to the weather service."}
    except requests.exceptions.Timeout:
        return {"error": "The weather service took too long to respond."}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

# Initialize Flask app
app = Flask(__name__)

# Route to serve the HTML file
@app.route('/')
def home_route():
    try:
        # Serve the HTML file from the same directory
        return send_file('interface.html')
    except Exception as err:
        return f"Error serving the HTML file: {err}", 500

# Route to handle weather requests
@app.route('/weather', methods=['GET'])
def weather_route():
    try:
        city = request.args.get('city_name')  # Extract city name from query parameters
        if not city:
            return jsonify({"error": "City parameter is required"}), 400

        data = get_weather(city)  # Fetch weather data
        if 'error' in data:
            return jsonify(data), 500  # Return any error from the `get_weather` function

        return jsonify(data), 200
    except Exception as err:
        return jsonify({"error": f"An unexpected server error occurred: {err}"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
