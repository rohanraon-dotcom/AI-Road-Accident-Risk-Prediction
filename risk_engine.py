def calculate_risk(weather, traffic, section):

    score = 0
    reasons = []
#Weather
    rain = weather.get("rain", 0)
    if rain > 10:
        score += 12
        reasons.append("Heavy rainfall")
    elif rain > 2:
        score += 7
        reasons.append("Rain")
    elif rain > 0:
        score += 3
        reasons.append("Light rain")

#Visiblity

    visibility = weather.get("visibility", 10000)

    visibility_km = visibility / 1000

    if visibility_km < 1:
        score += 10
        reasons.append("Very low visibility")

    elif visibility_km < 3:
        score += 6
        reasons.append("Reduced visibility")


#Wind
    wind = weather.get("wind_speed", 0)

    if wind > 50:
        score += 6
        reasons.append("Strong wind")

    elif wind > 30:
        score += 3
        reasons.append("High wind")


#Day/Night
    if weather.get("is_day", 1) == 0:
        score += 8
        reasons.append("Night driving")


#Traffic
    traffic_score = traffic.get("score", 5)

    score += traffic_score

    traffic_status = traffic.get(
        "status",
        "UNKNOWN"
    )

    if traffic_status == "JAM":
        reasons.append("Traffic jam")

    elif traffic_status == "HEAVY":
        reasons.append("Heavy traffic")

    elif traffic_status == "MODERATE":
        reasons.append("Moderate traffic")


#Road Geometry
    turns = section.get("turns", 0)

    sharp_turns = section.get(
        "sharp_turns",
        0
    )

    very_sharp = section.get(
        "very_sharp_turns",
        0
    )


    score += min(
        turns * 2,
        10
    )

    score += min(
        sharp_turns * 4,
        12
    )

    score += min(
        very_sharp * 5,
        10
    )


    if sharp_turns > 0:
        reasons.append(
            f"{sharp_turns} sharp curve(s)"
        )


    if very_sharp > 0:
        reasons.append(
            f"{very_sharp} very sharp curve(s)"
        )


#Ghat Like Road
    ghat_like = (
        sharp_turns >= 3
        and turns >= 6
    )

    if ghat_like:

        score += 8

        reasons.append(
            "Hilly / ghat-like road pattern"
        )


#Final Score
    score = min(
        round(score),
        100
    )


#Risk Level
    if score < 30:

        level = "LOW"

    elif score < 60:

        level = "MEDIUM"

    else:

        level = "HIGH"


    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }