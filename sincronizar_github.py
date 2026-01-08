# Arquivo: D:\projetos-inovexa\mindscan\sincronizar_github.py
# Status: Corrigido (Sem Emojis / UTF-8 Seguro)

import os
import json
import subprocess
import datetime
from pathlib import Path
from auditar_mindscan import auditar

ROOT = Path(__file__).resolve().parent
LOG = ROOT / ".mindscan_orchestrator.log"

def log_event(event, data):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event,
        "data": data,
    }
    try:
        current = LOG.read_text(encoding='utf-8') if LOG.exists() else ""
        LOG.write_text(current + json.dumps(entry, ensure_ascii=False) + "\n", encoding='utf-8')
    except:
        pass

def run(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ROOT, encoding='utf-8')
        return result.stdout.strip(), result.stderr.strip()
    except:
        return "", "Erro de execução"

def sincronizar():
    print("[START] ORQUESTRADOR MINDSCAN")
    
    # 1. Auditoria
    audit = auditar()
    if audit["risk_assessment"]["level"] == "ALTO":
        print("!!! RISCO ALTO DETECTADO. ABORTANDO PUSH !!!")
        return

    # 2. Git Workflow
    print("Sincronizando com GitHub...")
    run("git add .")
    commit_msg = f"Sync {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | Risco: {audit['risk_assessment']['level']}"
    run(f'git commit -m "{commit_msg}"')
    
    stdout, stderr = run("git push origin main")
    
    if "Everything up-to-date" in stdout or not stderr:
        print("SUCESSO: GitHub Sincronizado.")
    else:
        print(f"AVISO: Verificar estado do push: {stderr}")

    log_event("sync_result", {"msg": "Pipeline finalizado"})

if __name__ == "__main__":
    sincronizar()