import os
import json
import psutil
import gzip
import shutil
import requests
from datetime import datetime
from pathlib import Path

# ============================================
# 🧠 MindScan Audit Reporter — v5.0
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Geração e envio automático de relatórios de auditoria
# ============================================

BASE_DIR = Path(r"D:\MindScan")
LOG_DIR = BASE_DIR / "logs"
MANIFEST_PATH = BASE_DIR / "update_manifest.json"
REPORT_DIR = BASE_DIR / "reports"
REMOTE_ENDPOINT = "https://commandcenter.inovexa.ai/api/audit/upload"
AUTH_TOKEN = os.getenv("INOVEXA_AUDIT_TOKEN", "DEV-TOKEN")

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------- UTILITÁRIOS ----------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    print(f"[{now()}] [AuditReporter] {msg}")

def load_manifest():
    if not MANIFEST_PATH.exists():
        return {}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def collect_system_info():
    return {
        "timestamp": now(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage(str(BASE_DIR)).percent,
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "services_running": len(psutil.pids())
    }

def collect_logs(limit=200):
    logs = []
    for file in sorted(LOG_DIR.glob("*.log"), reverse=True):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[-limit:]
        logs.extend([{"file": file.name, "entry": l.strip()} for l in lines])
    return logs[-limit:]

# ---------------------- RELATÓRIO ----------------------
def generate_audit_report():
    log("Gerando relatório de auditoria MindScan...")
    manifest = load_manifest()
    sys_info = collect_system_info()
    logs = collect_logs()

    report_data = {
        "system": "MindScan Web",
        "generated_at": now(),
        "version": manifest.get("current_build", {}).get("version_tag", "desconhecida"),
        "integrity": manifest.get("verification", {}).get("last_result", "indefinida"),
        "rollback_status": manifest.get("rollback", {}).get("enabled", False),
        "sys_info": sys_info,
        "log_count": len(logs),
        "logs": logs,
        "update_history": manifest.get("update_history", [])
    }

    filename_base = f"Audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    json_path = REPORT_DIR / f"{filename_base}.json"
    md_path = REPORT_DIR / f"{filename_base}.md"

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(report_data, jf, indent=2, ensure_ascii=False)

    # Markdown version
    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write(f"# 🧠 MindScan Audit Report — {now()}\n\n")
        mf.write(f"**Versão:** {report_data['version']}\n")
        mf.write(f"**Integridade:** {report_data['integrity']}\n")
        mf.write(f"**Rollback Ativo:** {report_data['rollback_status']}\n")
        mf.write(f"**CPU:** {sys_info['cpu_usage']}% | **Memória:** {sys_info['memory_usage']}% | **Disco:** {sys_info['disk_usage']}%\n")
        mf.write(f"**Serviços em execução:** {sys_info['services_running']}\n\n")
        mf.write("## Histórico de Atualizações\n")
        for u in report_data["update_history"]:
            mf.write(f"- {u['version']} — {u['applied_at']} — {u['result']}\n")
        mf.write("\n## Últimos Logs\n")
        for l in logs[-20:]:
            mf.write(f"- `{l['file']}`: {l['entry']}\n")

    log(f"Relatório gerado: {md_path}")
    return json_path, md_path

# ---------------------- ENVIO ----------------------
def compress_and_send(json_path):
    gz_path = json_path.with_suffix(".json.gz")
    with open(json_path, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    log(f"Arquivo compactado: {gz_path}")

    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    files = {"file": open(gz_path, "rb")}
    data = {"system": "MindScan Web", "timestamp": now()}

    try:
        resp = requests.post(REMOTE_ENDPOINT, headers=headers, files=files, data=data, timeout=10)
        if resp.status_code == 200:
            log("Relatório enviado ao Command Center com sucesso.")
        else:
            log(f"Falha ao enviar relatório: {resp.status_code}")
    except Exception as e:
        log(f"Erro de envio: {e}")

# ---------------------- EXECUÇÃO ----------------------
def main():
    json_path, md_path = generate_audit_report()
    compress_and_send(json_path)
    log("Ciclo de auditoria concluído.")

if __name__ == "__main__":
    main()
