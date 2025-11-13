import os
import time
import psutil
import requests
import threading
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from plyer import notification
from PIL import Image, ImageDraw
import pystray

# ============================================
# 🧠 MindScan Sentinel Daemon — v5.7
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Serviço híbrido residente (monitor + bandeja)
# ============================================

LOG_API = "http://127.0.0.1:8091/logs"
REMOTE_CONSOLE = "http://127.0.0.1:8093"
DASHBOARD_PATH = Path(r"D:\MindScan\core\MindScan_SentinelIntegration.py")
DASHBOARD_URL = "http://127.0.0.1:8095"
AUTH_TOKEN = os.getenv("INOVEXA_CONSOLE_KEY", "DEV-LOCAL-KEY")
ICON_COLOR = "#2563EB"
CHECK_INTERVAL = 60  # segundos

# ---------------------- LOG E NOTIFICAÇÃO ----------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, level="INFO"):
    print(f"[{now()}] [SentinelDaemon] [{level}] {msg}")
    try:
        requests.post(LOG_API, json={"origin": "SentinelDaemon", "message": msg, "level": level}, timeout=1)
    except Exception:
        pass

def notify(title, message):
    try:
        notification.notify(title=title, message=message, timeout=4, app_name="MindScan Sentinel")
    except Exception:
        pass

# ---------------------- FUNÇÕES CORE ----------------------
def dashboard_running():
    for p in psutil.process_iter(['cmdline']):
        try:
            if p.info['cmdline'] and "MindScan_SentinelIntegration.py" in " ".join(p.info['cmdline']):
                return True
        except Exception:
            continue
    return False

def ensure_dashboard():
    if not dashboard_running():
        log("Painel Sentinel inativo. Reiniciando...", "WARN")
        subprocess.Popen(["python", str(DASHBOARD_PATH)], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(5)
        if dashboard_running():
            notify("MindScan Sentinel", "Painel reiniciado com sucesso.")
            log("Painel reiniciado.")
        else:
            notify("MindScan Sentinel", "Falha ao reiniciar o painel.")
            log("Falha ao reiniciar painel Sentinel.", "ERROR")

def check_resources():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    if cpu > 95:
        notify("MindScan Sentinel", f"Uso de CPU elevado: {cpu}%")
        log(f"CPU elevada detectada: {cpu}%", "WARN")
    if mem > 90:
        notify("MindScan Sentinel", f"Uso de memória elevado: {mem}%")
        log(f"Memória elevada detectada: {mem}%", "WARN")

def restart_services():
    try:
        r = requests.post(f"{REMOTE_CONSOLE}/restart", headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, timeout=5)
        if r.status_code == 200:
            notify("MindScan Sentinel", "Serviços reiniciados.")
            log("Serviços reiniciados via Daemon.")
        else:
            notify("MindScan Sentinel", "Falha ao reiniciar serviços.")
    except Exception as e:
        log(f"Erro no restart: {e}", "ERROR")

def force_sync():
    try:
        r = requests.post(f"{REMOTE_CONSOLE}/sync", headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, timeout=5)
        if r.status_code == 200:
            notify("MindScan Sentinel", "Sincronização concluída.")
            log("Sync forçado via Daemon.")
        else:
            notify("MindScan Sentinel", "Falha na sincronização.")
    except Exception as e:
        log(f"Erro no sync: {e}", "ERROR")

def trigger_rollback():
    try:
        r = requests.post(f"{REMOTE_CONSOLE}/rollback", headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, timeout=5)
        if r.status_code == 200:
            notify("MindScan Sentinel", "Rollback executado.")
            log("Rollback remoto via Daemon.")
        else:
            notify("MindScan Sentinel", "Falha no rollback.")
    except Exception as e:
        log(f"Erro no rollback: {e}", "ERROR")

# ---------------------- MONITORAMENTO ----------------------
def monitor_loop():
    log("Monitoramento iniciado (modo contínuo).")
    while True:
        ensure_dashboard()
        check_resources()
        time.sleep(CHECK_INTERVAL)

# ---------------------- ÍCONE DE BANDEJA ----------------------
def create_icon():
    img = Image.new("RGB", (64, 64), color=ICON_COLOR)
    draw = ImageDraw.Draw(img)
    draw.ellipse((10, 10, 54, 54), fill="#60A5FA")
    draw.text((25, 22), "M", fill="white")
    return img

def open_dashboard(icon, item=None):
    webbrowser.open(DASHBOARD_URL)
    log("Painel aberto via bandeja.")

def show_status(icon, item=None):
    try:
        r = requests.get(f"{REMOTE_CONSOLE}/status", headers={"Authorization": f"Bearer {AUTH_TOKEN}"}, timeout=5)
        if r.status_code == 200:
            s = r.json()
            msg = f"CPU: {s['cpu']}% | Mem: {s['memory']}% | Proc: {s['processes']}"
            notify("Status MindScan", msg)
        else:
            notify("MindScan Sentinel", "Falha ao obter status.")
    except Exception:
        notify("MindScan Sentinel", "Console remoto inacessível.")

def exit_app(icon, item=None):
    log("SentinelDaemon encerrado pelo usuário.", "WARN")
    notify("MindScan Sentinel", "Daemon encerrado.")
    icon.stop()
    os._exit(0)

def tray_loop():
    icon = pystray.Icon(
        "MindScan Sentinel",
        create_icon(),
        menu=pystray.Menu(
            pystray.MenuItem("Abrir Painel", open_dashboard),
            pystray.MenuItem("Exibir Status", show_status),
            pystray.MenuItem("Forçar Sync", lambda icon, item: force_sync()),
            pystray.MenuItem("Rollback", lambda icon, item: trigger_rollback()),
            pystray.MenuItem("Reiniciar Serviços", lambda icon, item: restart_services()),
            pystray.MenuItem("Sair", exit_app)
        )
    )
    icon.run()

# ---------------------- MAIN ----------------------
def main():
    log("SentinelDaemon inicializado.")
    notify("MindScan Sentinel", "Daemon residente iniciado.")
    t1 = threading.Thread(target=monitor_loop, daemon=True)
    t2 = threading.Thread(target=tray_loop, daemon=False)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("SentinelDaemon encerrado manualmente.", "WARN")
        notify("MindScan Sentinel", "Daemon encerrado manualmente.")
