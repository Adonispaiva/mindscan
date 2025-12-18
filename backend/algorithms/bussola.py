def run(payload: dict) -> dict:
    raw_scores = payload.get("scores", {})
    orientation = {}

    for key, value in raw_scores.items():
        orientation[key] = float(value)

    return {
        "module": "bussola",
        "orientation": orientation
    }
