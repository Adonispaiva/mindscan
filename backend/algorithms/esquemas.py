def run(payload: dict) -> dict:
    schemas = payload.get("schemas", {})

    return {
        "module": "esquemas",
        "schemas": schemas
    }
