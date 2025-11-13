import os
import json
from datetime import datetime

ROOT_PATH = r"D:\projetos-inovexa\mindscan"
LOGS_DIR = os.path.join(ROOT_PATH, "logs")
REPORT_FILE = os.path.join(ROOT_PATH, "docs", f"mindscan_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

def collect_logs():
    logs = []
    for root, _, files in os.walk(LOGS_DIR):
        for file in files:
            if file.endswith(".json") or file.endswith(".log"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                        logs.append({"file": file, "content": content})
                except Exception as e:
                    logs.append({"file": file, "content": f"[Erro ao ler arquivo: {e}]"})
    return logs

def generate_report():
    logs = collect_logs()
    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write(f"# 🧠 MindScan — Relatório Pós-Deploy\n\n")
        report.write(f"**Data:** {datetime.now()}\n\n")
        report.write(f"**Caminho Base:** `{ROOT_PATH}`\n\n")
        report.write("## 📋 Logs Consolidados\n\n")
        for log in logs:
            report.write(f"### {log['file']}\n```\n{log['content']}\n```\n\n")
    print(f"📘 Relatório consolidado gerado em: {REPORT_FILE}")

if __name__ == "__main__":
    print("Gerando relatório pós-deploy do MindScan...")
    generate_report()
    print("Relatório finalizado com sucesso.")
