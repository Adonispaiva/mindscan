import subprocess
import sys

# Passo 1: Garantir que o 'requests' esteja instalado
try:
    import requests
except ImportError:
    print("📦 Instalando módulo 'requests'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Passo 2: Testar o endpoint da API
URL = "http://localhost:8000"
print(f"🔍 Testando acesso a: {URL}")

try:
    response = requests.get(URL, timeout=5)
    print(f"✅ Resposta recebida! Status: {response.status_code}")
    print("Conteúdo:")
    print(response.text[:500])
except requests.exceptions.ConnectionError:
    print("❌ Falha de conexão: não foi possível acessar http://localhost:8000")
except requests.exceptions.Timeout:
    print("❌ Tempo limite excedido ao tentar conectar.")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")
