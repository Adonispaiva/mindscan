# D:\projetos-inovexa\mindscan\scripts\policy_loader.py
import json
from pathlib import Path

CONFIG_PATH = Path("D:/projetos-inovexa/mindscan/config/validator_policy.json")

def load_policy():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    print(json.dumps(load_policy(), indent=4))
