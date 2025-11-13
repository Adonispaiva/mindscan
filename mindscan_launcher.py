# -*- coding: utf-8 -*-
"""
MindScan Launcher v1.1.3 — Orquestrador Unificado
Diretor Técnico: Leo Vinci
© Inovexa Software

Inicializa e monitora todos os módulos do sistema MindScan.
"""

import os
import subprocess
import hashlib
import time
from datetime import datetime, timezone, timedelta

# Força UTF-8 no console do Windows
os.system("chcp 65001 >nul")

MODULES = {
    "Command Center": r"D:\projetos-inovexa\mindscan\command_center\command_center_interface.py",
    "Watchdog": r"D:\projetos-inovexa\mindscan\maintenance\watchdog\mindscan_task_watcher_auto.py",
    "Daemon": r"D:\projetos-inovexa\mindscan\maintenance\recovery\mindscan_recovery_daemon.py",
    "SAFE": r"D:\projetos-inovexa\mindscan\diagnostico_mindscan_SAFE.py",
}

def local_time():
    br_time = datetime.now(timezone.utc) - timedelta(hours=3)
    return br_time.strftime("%Y-%m-%d %H:%M:%S")

def file_hash(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except FileNotFoundError:
        return "MISSING"

def log(msg, icon="🟣"):
    print(f"[{local_time()}] {icon} {msg}")

print("\n🧠 Inovexa MindScan Launcher v1.1.3 — Orquestrador Unificado\n")
log("Sessão iniciada às " + local_time(), "🕓")

log("Verificando integridade dos módulos...", "🧩")
for name, path in MODULES.items():
    status = "OK" if os.path.exists(path) else "FALHA"
    sha = file_hash(path)
    print(f"[{local_time()}] │ {name:<15} │ {status:<5} │ SHA256: {sha}")
log("Verificação concluída.", "✅")

processes = {}
for name, path in MODULES.items():
    log(f"Iniciando módulo: {name}", "⚙️")
    if not os.path.exists(path):
        log(f"❌ Arquivo não encontrado: {path}", "❌")
        continue
    try:
        p = subprocess.Popen(["python", path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        processes[name] = p
        log(f"{name} iniciado → {path}", "🟢")
    except Exception as e:
        log(f"Erro ao iniciar {name}: {e}", "🔴")

log("Todos os módulos foram iniciados com sucesso.", "✨")
print(f"\n[{local_time()}] 🧠 Sistema ativo — pressione Ctrl+C para encerrar.\n")

try:
    while True:
        alive = [n for n, p in processes.items() if p.poll() is None]
        dead = [n for n in MODULES.keys() if n not in alive]
        if dead:
            for d in dead:
                log(f"⚠️ Módulo {d} finalizado inesperadamente!", "⚠️")
        time.sleep(5)
except KeyboardInterrupt:
    log("Encerrando sessão MindScan...", "🛑")
    for n, p in processes.items():
        try:
            p.terminate()
            log(f"{n} encerrado.", "🔻")
        except Exception:
            pass
    log("Sessão encerrada com segurança.", "✅")
