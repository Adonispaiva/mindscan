import requests

URL = "http://localhost:8000"

print(f"🔍 Testando acesso a: {URL}")

try:
    response = requests.get(URL, timeout=5)
    print(f"✅ Resposta recebida! Status: {response.status_code}")
    print("Conteúdo:")
    print(response.text[:500])  # Mostra os primeiros 500 caracteres da resposta
except requests.exceptions.ConnectionError:
    print("❌ Falha de conexão: não foi possível acessar http://localhost:8000")
except requests.exceptions.Timeout:
    print("❌ Tempo limite excedido ao tentar conectar.")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")
