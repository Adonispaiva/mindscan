def run(payload: dict) -> dict:
    data = payload.get("data", {})

    crossings = {}
    keys = list(data.keys())

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            k1, k2 = keys[i], keys[j]
            crossings[f"{k1}_x_{k2}"] = data[k1] * data[k2]

    return {
        "module": "cruzamentos",
        "results": crossings
    }
