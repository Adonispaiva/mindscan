import subprocess
import time
import requests
from datetime import datetime

LOG_PATH = "relatorio_execucao.txt"

def escrever_log(msg):
    timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
    with open(LOG_PATH, "a") as f:
        f.write(f"{timestamp} {msg}\n")
    print(f"{timestamp} {msg}")

def subir_containers():
    escrever_log("Iniciando build dos containers Docker...")
    subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
    escrever_log("Containers iniciados.")

def testar_backend():
    url = "http://localhost:8000/status"
    escrever_log(f"Testando endpoint: {url}")
    for tentativa in range(10):
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                escrever_log(f"✅ Backend responde: {response.json()}")
                return True
        except Exception as e:
            escrever_log(f"Tentativa {tentativa + 1}/10 falhou: {e}")
        time.sleep(2)
    escrever_log("❌ Backend não respondeu após 10 tentativas.")
    return False

def main():
    escrever_log("=== Início da Verificação MindScan ===")
    try:
        subir_containers()
        status_backend = testar_backend()
        if status_backend:
            escrever_log("🎯 Sistema MindScan OK para testes externos.")
        else:
            escrever_log("⚠️ Falha na resposta do backend.")
    except Exception as e:
        escrever_log(f"Erro durante execução: {e}")
    escrever_log("=== Fim da Verificação ===\n")

if __name__ == "__main__":
    main()
