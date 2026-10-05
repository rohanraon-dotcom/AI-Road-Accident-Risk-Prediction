from flask import Flask, render_template, request, jsonify

from geocoder import geocode
from route_analyzer import get_route, create_sections
from weather import get_weather
from traffic import get_traffic
from risk_engine import calculate_risk
from database import init_db, save_journey, get_history


app = Flask(__name__)

init_db()


def middle_coordinate(coordinates):

    index = len(coordinates) // 2

    point = coordinates[index]

    return {
        "lat": point[1],
        "lon": point[0]
    }


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        source_name = data.get(
            "source",
            ""
        ).strip()

        destination_name = data.get(
            "destination",
            ""
        ).strip()


        if not source_name or not destination_name:

            return jsonify({
                "error":
                "Source and destination are required."
            }), 400


        # -----------------------------
        # GEOCODING
        # -----------------------------

        source = geocode(
            source_name
        )

        destination = geocode(
            destination_name
        )


        # -----------------------------
        # ROUTE GENERATION
        # -----------------------------

        route = get_route(
            source,
            destination
        )


        # -----------------------------
        # CREATE SECTIONS
        # -----------------------------

        sections = create_sections(
            route,
            number_of_sections=6
        )


        analyzed_sections = []


        # -----------------------------
        # ANALYZE EACH SECTION
        # -----------------------------

        for section in sections:

            center = middle_coordinate(
                section["coordinates"]
            )


            # Weather

            weather = get_weather(
                center["lat"],
                center["lon"]
            )


            # Traffic

            traffic = get_traffic(
                center["lat"],
                center["lon"]
            )


            # Risk

            risk = calculate_risk(
                weather,
                traffic,
                section
            )


            analyzed_sections.append({

                "id":
                    section["id"],

                "coordinates":
                    section["coordinates"],

                "turns":
                    section["turns"],

                "sharp_turns":
                    section["sharp_turns"],

                "very_sharp_turns":
                    section["very_sharp_turns"],

                "weather":
                    weather,

                "traffic":
                    traffic,

                "risk":
                    risk
            })


        # -----------------------------
        # OVERALL RISK
        # -----------------------------

        scores = [

            section["risk"]["score"]

            for section
            in analyzed_sections
        ]


        if scores:

            overall_score = round(
                sum(scores) /
                len(scores)
            )

        else:

            overall_score = 0


        # Find highest-risk section

        highest_section = max(
            analyzed_sections,
            key=lambda x:
            x["risk"]["score"]
        )


        # Risk level

        if overall_score < 30:

            overall_level = "LOW"

        elif overall_score < 60:

            overall_level = "MEDIUM"

        else:

            overall_level = "HIGH"


        # -----------------------------
        # SAVE JOURNEY
        # -----------------------------

        save_journey(

            source_name,

            destination_name,

            route["distance"] / 1000,

            route["duration"] / 60,

            overall_score,

            overall_level,

            highest_section["id"]
        )


        # -----------------------------
        # SEND RESULT TO FRONTEND
        # -----------------------------

        return jsonify({

            "source":
                source,

            "destination":
                destination,

            "distance":
                round(
                    route["distance"] / 1000,
                    2
                ),

            "duration":
                round(
                    route["duration"] / 60
                ),

            "geometry":
                route["geometry"],

            "sections":
                analyzed_sections,

            "overall": {

                "score":
                    overall_score,

                "level":
                    overall_level,

                "highest_section":
                    highest_section["id"]
            }
        })


    except Exception as error:

        print(error)

        return jsonify({

            "error":
                str(error)

        }), 500


@app.route("/history")
def history():

    return jsonify(
        get_history()
    )


if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000
    )