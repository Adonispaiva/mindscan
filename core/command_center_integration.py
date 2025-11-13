import os
import time
import json
import requests
from datetime import datetime
import sys

# ============================================
# Command Center Integration — v4.1
# Comunicação segura com o Inovexa Command Center
# ============================================

API_URL = "https://commandcenter.inovexa.ai/api/mindscan/upload"
API_KEY = os.getenv("INOVEXA_API_KEY", "DEV-LOCAL-KEY")
REPORT_PATH = "D:\\MindScan\\supervisao_diretor.md"
CACHE_DIR = "D:\\MindScan\\cache"
INTERVAL = 1800  # 30 minutos

def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, level="INFO"):
    line = f"[{now()}] [CommandCenter] [{level}] {msg}"
    print(line)
    sys.stdout.flush()

    try:
        requests.post(
            "http://127.0.0.1:8091/logs",
            json={"origin": "CommandCenter", "message": msg, "level": level},
            timeout=1,
        )
    except Exception:
        pass

def cache_unsent(data):
    """Salva relatórios não enviados localmente para envio posterior."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"unsent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write(data)
    log(f"Relatório armazenado no cache: {cache_file}", "WARN")

def send_to_command_center(content):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "timestamp": now(),
        "system": "MindScan",
        "version": "4.1",
        "report": content,
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            log("Relatório enviado ao Command Center com sucesso.", "INFO")
            return True
        else:
            log(f"Falha ao enviar relatório: {response.status_code} - {response.text}", "ERROR")
            return False
    except Exception as e:
        log(f"Erro de comunicação: {e}", "ERROR")
        return False

def loop():
    log("Iniciando integração com Command Center.")
    while True:
        try:
            if not os.path.exists(REPORT_PATH):
                log("Arquivo supervisao_diretor.md não encontrado.", "WARN")
                time.sleep(INTERVAL)
                continue

            with open(REPORT_PATH, "r", encoding="utf-8") as f:
                content = f.read()

            success = send_to_command_center(content)
            if not success:
                cache_unsent(content)

        except Exception as e:
            log(f"Erro inesperado: {e}", "ERROR")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        log("Integração interrompida manualmente.", "WARN")
