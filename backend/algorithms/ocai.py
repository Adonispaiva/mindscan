def run(payload: dict) -> dict:
    culture = payload.get("culture", {})

    dominant = max(culture, key=culture.get) if culture else None

    return {
        "module": "ocai",
        "dominant_culture": dominant,
        "scores": culture
    }
