def run(payload: dict) -> dict:
    scores = payload.get("scores", {})

    return {
        "module": "dass21",
        "depression": float(scores.get("depression", 0)),
        "anxiety": float(scores.get("anxiety", 0)),
        "stress": float(scores.get("stress", 0)),
    }
