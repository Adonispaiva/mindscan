import os
import json
import shutil
from datetime import datetime
from collections import defaultdict

ROOT_PATH = r"D:\projetos-inovexa\mindscan"
REPORT_PATH = os.path.join(ROOT_PATH, "docs", f"mindscan_weight_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
SUMMARY_PATH = os.path.join(ROOT_PATH, "docs", "mindscan_weight_summary.txt")

EXCLUDE_DIRS = [
    ".git", "__pycache__", ".idea", ".vscode", ".pytest_cache",
    "node_modules", ".venv", "env", "venv"
]

def get_size(path):
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path, topdown=True):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    if os.path.islink(fp):
                        continue
                    total_size += os.path.getsize(fp)
                except Exception:
                    pass
    except Exception:
        pass
    return total_size

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"

def audit_directories(root_path):
    dir_sizes = defaultdict(int)
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            dir_sizes[item] = get_size(item_path)
        elif os.path.isfile(item_path):
            dir_sizes[item] = os.path.getsize(item_path)
    return dict(sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True))

def suggest_cleanup(data):
    suggestions = []
    if "backup" in data and data["backup"] > 5 * (1024**3):
        suggestions.append("⚠️ Backup excede 5 GB. Recomenda-se remover versões antigas (>15 dias).")
    if "logs" in data and data["logs"] > 1 * (1024**3):
        suggestions.append("⚠️ Logs excedem 1 GB. Compactar ou limpar logs antigos.")
    if "venv" in data or "env" in data:
        suggestions.append("💡 Verifique ambientes duplicados (venv/env). Mantenha apenas um.")
    if "frontend" in data and data["frontend"] > 2 * (1024**3):
        suggestions.append("💡 node_modules está muito pesado. Execute 'npm clean-install'.")
    if not suggestions:
        suggestions.append("✅ Nenhum diretório excede o limite esperado.")
    return suggestions

def generate_report():
    print("🔍 Calculando tamanhos de diretórios, aguarde...")
    results = audit_directories(ROOT_PATH)
    total = sum(results.values())

    report_data = {
        "root_path": ROOT_PATH,
        "timestamp": datetime.now().isoformat(),
        "total_size_bytes": total,
        "total_size_human": sizeof_fmt(total),
        "directory_sizes": {k: sizeof_fmt(v) for k, v in results.items()},
        "cleanup_suggestions": suggest_cleanup(results)
    }

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False)

    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write(f"📦 RELATÓRIO DE PESO — MINDSCAN ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n")
        for k, v in report_data["directory_sizes"].items():
            f.write(f"{k:<20} {v}\n")
        f.write("\n---\n")
        f.write(f"TOTAL: {report_data['total_size_human']}\n\n")
        f.write("💡 Sugestões de limpeza:\n")
        for s in report_data["cleanup_suggestions"]:
            f.write(f" - {s}\n")

    print(f"✅ Relatório gerado em:\n  {REPORT_PATH}\n  {SUMMARY_PATH}")
    print("💡 Leia o resumo para saber quais pastas mais pesam no projeto.")

if __name__ == "__main__":
    generate_report()
{\rtf1}