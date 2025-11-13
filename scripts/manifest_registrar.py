import os
import json
import hashlib
from datetime import datetime

ROOT_PATH = r"D:\projetos-inovexa\mindscan"
MANIFEST_FILE = os.path.join(ROOT_PATH, "docs", f"manifest_mindscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

EXCLUDE_DIRS = ["backup", "logs", "__pycache__", ".git"]

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def generate_manifest():
    manifest = {
        "generated_at": str(datetime.now()),
        "root_path": ROOT_PATH,
        "files": []
    }

    for root, dirs, files in os.walk(ROOT_PATH):
        if any(ex in root for ex in EXCLUDE_DIRS):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            try:
                stat = os.stat(file_path)
                manifest["files"].append({
                    "path": os.path.relpath(file_path, ROOT_PATH),
                    "size_bytes": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "hash": hash_file(file_path)
                })
            except Exception as e:
                manifest["files"].append({
                    "path": file_path,
                    "error": str(e)
                })

    os.makedirs(os.path.dirname(MANIFEST_FILE), exist_ok=True)
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)

    print(f"🗂️ Manifesto gerado com sucesso em: {MANIFEST_FILE}")

if __name__ == "__main__":
    print("Gerando manifesto completo do projeto MindScan...")
    generate_manifest()
    print("Manifesto finalizado.")
