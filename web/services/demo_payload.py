def build_demo_payload(nome: str, email: str) -> dict:
    return {
        "user": {
            "name": nome,
            "email": email
        },
        "answers": {
            "q1": 3,
            "q2": 4,
            "q3": 2,
            "q4": 5
        },
        "metadata": {
            "source": "web_demo"
        }
    }
