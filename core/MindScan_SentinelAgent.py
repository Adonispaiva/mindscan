import os
import time
import psutil
import subprocess
import requests
import webbrowser
from plyer import notification
from datetime import datetime
from pathlib import Path

# ============================================
# 🧠 MindScan Sentinel Agent — v5.5
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Serviço residente com monitoramento e notificações locais
# ============================================

DASHBOARD_URL = "http://127.0.0.1:8095"
SENTINEL_PATH = Path(r"D:\MindScan\core\MindScan_SentinelIntegration.py")
LOG_API = "http://127.0.0.1:8091/logs"
CHECK_INTERVAL = 60  # segundos

def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, level="INFO"):
    print(f"[{now()}] [SentinelAgent] [{level}] {msg}")
    try:
        requests.post(LOG_API, json={"origin": "SentinelAgent", "message": msg, "level": level}, timeout=1)
    except Exception:
        pass

def notify(title, message):
    """Tenta mostrar uma notificação local, com fallback em beep."""
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5,
            app_name="MindScan Sentinel"
        )
    except Exception:
        try:
            import winsound
            winsound.Beep(1000, 400)
        except Exception:
            pass

def is_dashboard_running():
    """Verifica se o painel Sentinel está ativo."""
    for p in psutil.process_iter(['name', 'cmdline']):
        try:
            if 'MindScan_SentinelIntegration.py' in ' '.join(p.info['cmdline']):
                return True
        except Exception:
            continue
    return False

def ensure_dashboard():
    """Mantém o painel Flask ativo."""
    if not is_dashboard_running():
        log("Painel Sentinel inativo. Tentando reiniciar...", "WARN")
        subprocess.Popen(["python", str(SENTINEL_PATH)], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(5)
        if is_dashboard_running():
            log("Painel Sentinel reiniciado com sucesso.", "INFO")
            notify("MindScan Sentinel", "Painel reiniciado e ativo.")
        else:
            log("Falha ao reiniciar o painel Sentinel.", "ERROR")
            notify("MindScan Sentinel", "Erro ao iniciar o painel.")

def open_browser_once():
    """Abre o painel no navegador padrão se ainda não estiver aberto."""
    try:
        import socket
        s = socket.socket()
        s.settimeout(1)
        try:
            s.connect(("127.0.0.1", 8095))
            s.close()
            webbrowser.open(DASHBOARD_URL)
            log("Painel Sentinel aberto no navegador padrão.")
        except Exception:
            pass
    except Exception:
        log("Falha ao abrir navegador automaticamente.", "WARN")

def main():
    log("Sentinel Agent iniciado.")
    notify("MindScan Sentinel", "Agente residente iniciado e em monitoramento.")
    open_browser_once()
    while True:
        ensure_dashboard()
        # Checa anomalias de CPU e memória
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        if cpu > 95:
            log(f"Uso alto de CPU detectado: {cpu}%", "WARN")
            notify("MindScan Sentinel", f"CPU elevada: {cpu}%")
        if mem > 90:
            log(f"Uso alto de memória detectado: {mem}%", "WARN")
            notify("MindScan Sentinel", f"Memória alta: {mem}%")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Sentinel Agent encerrado manualmente.", "WARN")
        notify("MindScan Sentinel", "Agente encerrado manualmente.")
