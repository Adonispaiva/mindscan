import requests
from backend.utils.demo_payload import DEMO_PAYLOAD

URL = "http://127.0.0.1:8000/mindscan/run"

response = requests.post(URL, json=DEMO_PAYLOAD)

print("Status:", response.status_code)
print("Resposta:", response.json())
