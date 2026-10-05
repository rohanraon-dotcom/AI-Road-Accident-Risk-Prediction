import requests

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(lat, lon):

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain,"
            "visibility,"
            "wind_speed_10m,"
            "wind_gusts_10m,"
            "is_day,"
            "weather_code"
        ),
        "timezone": "auto"
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    current = data.get("current", {})

    return {
        "temperature": current.get("temperature_2m", 0),
        "humidity": current.get("relative_humidity_2m", 0),
        "precipitation": current.get("precipitation", 0),
        "rain": current.get("rain", 0),
        "visibility": current.get("visibility", 10000),
        "wind_speed": current.get("wind_speed_10m", 0),
        "wind_gust": current.get("wind_gusts_10m", 0),
        "is_day": current.get("is_day", 1),
        "weather_code": current.get("weather_code", 0)
    }