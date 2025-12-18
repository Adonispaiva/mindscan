def run(payload: dict) -> dict:
    scores = payload.get("scores", {})
    result = {}

    for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
        result[trait] = float(scores.get(trait, 0))

    return {
        "module": "big5",
        "scores": result
    }
