import requests
import time

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "AI-Road-Accident-Risk-Demo/1.0"
}


def geocode(place):
    params = {
        "q": place,
        "format": "json",
        "limit": 1
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError(f"Location not found: {place}")

    result = data[0]

    time.sleep(1)

    return {
        "lat": float(result["lat"]),
        "lon": float(result["lon"]),
        "name": result.get("display_name", place)
    }