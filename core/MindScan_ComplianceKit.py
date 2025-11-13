import os
import re
import json
import gzip
import shutil
import requests
from pathlib import Path
from datetime import datetime

# ============================================
# ⚖️ MindScan ComplianceKit — v5.1
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Auditoria de conformidade + anonimização ativa + reporte remoto
# ============================================

BASE_DIR = Path(r"D:\MindScan")
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "datasets"
CACHE_DIR = BASE_DIR / "cache"
REPORT_DIR = BASE_DIR / "reports"

REMOTE_ENDPOINT = "https://commandcenter.inovexa.ai/api/compliance/report"
AUTH_TOKEN = os.getenv("INOVEXA_COMPLIANCE_TOKEN", "DEV-TOKEN")

PATTERNS = {
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}\-\d{2}\b",
    "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "Telefone": r"\b(\+55\s?)?(\(?\d{2}\)?\s?)?\d{4,5}[- ]?\d{4}\b",
    "IP": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "Nome": r"\b[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]+\s+[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]+\b"
}

ANONYMIZE_TOKEN = "***MASKED***"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------- UTILITÁRIOS ----------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    print(f"[{now()}] [ComplianceKit] {msg}")

def scan_file(file_path):
    findings = []
    text = ""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        for label, pattern in PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                findings.append({"type": label, "count": len(matches)})
        return findings
    except Exception as e:
        log(f"Erro ao escanear {file_path}: {e}")
        return findings

def anonymize_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        for label, pattern in PATTERNS.items():
            text = re.sub(pattern, ANONYMIZE_TOKEN, text)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    except Exception as e:
        log(f"Erro ao anonimizar {file_path}: {e}")
        return False

def compress_file(file_path):
    gz_path = file_path.with_suffix(".gz")
    with open(file_path, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    return gz_path

# ---------------------- EXECUÇÃO ----------------------
def run_compliance_scan():
    log("Iniciando varredura de conformidade...")
    targets = [LOG_DIR, DATA_DIR, CACHE_DIR]
    report = {
        "timestamp": now(),
        "system": "MindScan Web",
        "action": "compliance_scan",
        "findings": [],
        "anonymized_files": 0,
        "total_files": 0
    }

    for target in targets:
        if not target.exists():
            continue
        for file in target.rglob("*.*"):
            if file.suffix.lower() in [".log", ".txt", ".json", ".csv"]:
                report["total_files"] += 1
                findings = scan_file(file)
                if findings:
                    report["findings"].append({"file": str(file), "issues": findings})
                    anonymize_file(file)
                    report["anonymized_files"] += 1

    log(f"Arquivos escaneados: {report['total_files']}, com {report['anonymized_files']} anonimizações.")

    # Salvar relatório
    filename = f"Compliance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json_path = REPORT_DIR / filename
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    gz_path = compress_file(json_path)
    send_report(gz_path, report)
    log("Ciclo de conformidade concluído.")
    return report

def send_report(gz_path, metadata):
    log("Enviando relatório ao Command Center...")
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    files = {"file": open(gz_path, "rb")}
    data = {"system": "MindScan Web", "timestamp": metadata["timestamp"], "findings": len(metadata["findings"])}

    try:
        resp = requests.post(REMOTE_ENDPOINT, headers=headers, files=files, data=data, timeout=10)
        if resp.status_code == 200:
            log("✅ Relatório de conformidade enviado com sucesso.")
        else:
            log(f"⚠️ Falha no envio: {resp.status_code}")
    except Exception as e:
        log(f"Erro de envio: {e}")

# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    run_compliance_scan()
