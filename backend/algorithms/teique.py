def run(payload: dict) -> dict:
    responses = payload.get("responses", [])

    total = sum(responses) if responses else 0

    return {
        "module": "teique",
        "emotional_intelligence": total
    }
