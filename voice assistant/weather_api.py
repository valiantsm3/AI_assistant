import requests

API_KEY = "your api key"  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            weather_info = (
                f"Weather in {city}: {weather_desc}. "
                f"Temperature: {temperature}°C. "
                f"Humidity: {humidity}%. "
                f"Wind Speed: {wind_speed} m/s."
            )
            return weather_info
        else:
            return f"City '{city}' not found. Please try again."
    
    except requests.exceptions.RequestException as e:
        return "Error fetching weather data. Please check your internet connection."
