def run(payload: dict) -> dict:
    indicators = payload.get("indicators", {})

    score = sum(indicators.values()) / len(indicators) if indicators else 0

    return {
        "module": "performance",
        "score": score,
        "indicators": indicators
    }
