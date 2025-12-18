def run(payload: dict) -> dict:
    profile_a = payload.get("profile_a", {})
    profile_b = payload.get("profile_b", {})

    matches = {}
    for key in profile_a:
        matches[key] = profile_a.get(key) == profile_b.get(key)

    return {
        "module": "matcher",
        "matches": matches
    }
