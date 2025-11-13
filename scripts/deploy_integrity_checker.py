import os
import hashlib
import json
from datetime import datetime

SOURCE_PATH = r"D:\projetos-inovexa\mindscan"
TARGET_PATH = r"D:\SynMind\deploy\MindScan"
LOG_FILE = os.path.join(SOURCE_PATH, "logs", f"deploy_integrity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def file_checksum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def compare_files():
    results = {"checked": [], "mismatched": [], "missing": [], "start": str(datetime.now())}

    for root, _, files in os.walk(SOURCE_PATH):
        for file in files:
            if "\\backup\\" in root or "\\logs\\" in root:
                continue
            source_file = os.path.join(root, file)
            rel_path = os.path.relpath(source_file, SOURCE_PATH)
            target_file = os.path.join(TARGET_PATH, rel_path)
            if not os.path.exists(target_file):
                results["missing"].append(rel_path)
                continue
            if file_checksum(source_file) != file_checksum(target_file):
                results["mismatched"].append(rel_path)
            results["checked"].append(rel_path)

    results["end"] = str(datetime.now())

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"✅ Verificação de integridade concluída. Log salvo em: {LOG_FILE}")

if __name__ == "__main__":
    print("Verificando integridade pós-deploy do MindScan...")
    compare_files()
    print("Processo concluído.")
