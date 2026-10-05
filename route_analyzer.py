import requests
import math

OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def get_route(source, destination):

    coordinates = (
        f"{source['lon']},{source['lat']};"
        f"{destination['lon']},{destination['lat']}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true"
    }

    response = requests.get(
        f"{OSRM_URL}/{coordinates}",
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError("Route could not be generated.")

    route = data["routes"][0]

    return route


def calculate_bearing(point1, point2):

    lat1 = math.radians(point1[1])
    lat2 = math.radians(point2[1])

    lon1 = math.radians(point1[0])
    lon2 = math.radians(point2[0])

    dlon = lon2 - lon1

    x = math.sin(dlon) * math.cos(lat2)

    y = (
        math.cos(lat1) * math.sin(lat2)
        - math.sin(lat1)
        * math.cos(lat2)
        * math.cos(dlon)
    )

    bearing = math.degrees(math.atan2(x, y))

    return (bearing + 360) % 360


def angle_difference(a, b):

    diff = abs(a - b)

    if diff > 180:
        diff = 360 - diff

    return diff


def analyze_turns(coordinates):

    if len(coordinates) < 3:
        return {
            "turns": 0,
            "sharp_turns": 0,
            "very_sharp_turns": 0
        }

    bearings = []

    for i in range(len(coordinates) - 1):
        bearings.append(
            calculate_bearing(
                coordinates[i],
                coordinates[i + 1]
            )
        )

    turns = 0
    sharp_turns = 0
    very_sharp_turns = 0

    for i in range(len(bearings) - 1):

        angle = angle_difference(
            bearings[i],
            bearings[i + 1]
        )

        if angle >= 20:
            turns += 1

        if angle >= 45:
            sharp_turns += 1

        if angle >= 70:
            very_sharp_turns += 1

    return {
        "turns": turns,
        "sharp_turns": sharp_turns,
        "very_sharp_turns": very_sharp_turns
    }


def create_sections(route, number_of_sections=6):

    coordinates = route["geometry"]["coordinates"]

    total_points = len(coordinates)

    number_of_sections = min(
        number_of_sections,
        total_points
    )

    sections = []

    chunk_size = max(
        2,
        math.ceil(total_points / number_of_sections)
    )

    section_id = 1

    for start in range(0, total_points, chunk_size):

        section_points = coordinates[
            start:start + chunk_size + 1
        ]

        if len(section_points) < 2:
            continue

        turn_data = analyze_turns(section_points)

        sections.append({
            "id": section_id,
            "coordinates": section_points,
            "turns": turn_data["turns"],
            "sharp_turns": turn_data["sharp_turns"],
            "very_sharp_turns": turn_data["very_sharp_turns"]
        })

        section_id += 1

    return sections