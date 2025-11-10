import subprocess
import sys

# Garantir que o 'requests' esteja instalado
try:
    import requests
except ImportError:
    print("📦 Instalando módulo 'requests'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Endpoints comuns para FastAPI ou APIs REST
endpoints = [
    "http://localhost:8000",
    "http://localhost:8000/",
    "http://localhost:8000/docs",
    "http://localhost:8000/health",
    "http://localhost:8000/status",
    "http://localhost:8000/api",
    "http://localhost:8000/api/health",
]

for url in endpoints:
    print(f"🔍 Testando: {url}")
    try:
        r = requests.get(url, timeout=5)
        print(f"✅ {url} respondeu com status {r.status_code}")
        print(r.text[:300], end="\n\n")
    except requests.exceptions.ConnectionError:
        print("❌ Conexão recusada.")
    except requests.exceptions.Timeout:
        print("❌ Tempo excedido.")
    except Exception as e:
        print(f"⚠️ Erro: {e}")
