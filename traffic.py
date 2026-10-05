import requests
from config import TOMTOM_API_KEY


def get_traffic(lat, lon):

    if not TOMTOM_API_KEY:
        return {
            "status": "UNAVAILABLE",
            "score": 5,
            "current_speed": None,
            "free_flow_speed": None
        }

    url = (
        "https://api.tomtom.com/traffic/services/4/"
        "flowSegmentData/absolute/10/json"
    )

    params = {
        "point": f"{lat},{lon}",
        "unit": "KMPH",
        "key": TOMTOM_API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        flow = data.get(
            "flowSegmentData",
            {}
        )

        current_speed = flow.get(
            "currentSpeed"
        )

        free_flow_speed = flow.get(
            "freeFlowSpeed"
        )

        if not current_speed or not free_flow_speed:

            return {
                "status": "UNKNOWN",
                "score": 5,
                "current_speed": current_speed,
                "free_flow_speed": free_flow_speed
            }

        ratio = current_speed / free_flow_speed

        if ratio >= 0.85:

            status = "FREE"
            score = 0

        elif ratio >= 0.65:

            status = "MODERATE"
            score = 8

        elif ratio >= 0.45:

            status = "HEAVY"
            score = 15

        else:

            status = "JAM"
            score = 20

        return {
            "status": status,
            "score": score,
            "current_speed": current_speed,
            "free_flow_speed": free_flow_speed
        }

    except Exception:

        return {
            "status": "UNAVAILABLE",
            "score": 5,
            "current_speed": None,
            "free_flow_speed": None
        }