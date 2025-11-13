"""
♻️ MindScan Update Agent — Template v5.8
Autor: Inovexa Software
Função: Verifica e aplica atualizações do MindScan de forma autônoma.
"""

import os, json, zipfile, requests, datetime, hashlib

UPDATE_URL = "https://updates.inovexa.local/mindscan/latest.zip"
TARGET_DIR = r"D:\MindScan"
MANIFEST_PATH = os.path.join(TARGET_DIR, "update_manifest.json")
LOG_PATH = os.path.join(TARGET_DIR, "logs", "update_agent.log")

def log(msg):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
    return h.hexdigest()

def download_update():
    log("Verificando atualização remota...")
    r = requests.get(UPDATE_URL, timeout=10)
    if r.status_code != 200:
        log(f"Falha ao baixar atualização: {r.status_code}")
        return None
    zip_path = os.path.join(TARGET_DIR, "mindscan_update.zip")
    with open(zip_path, "wb") as f: f.write(r.content)
    log(f"Atualização baixada: {zip_path}")
    return zip_path

def apply_update(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(TARGET_DIR)
    os.remove(zip_path)
    log("Atualização aplicada com sucesso.")

def main():
    zip_path = download_update()
    if zip_path:
        apply_update(zip_path)
        manifest = {"updated_at": datetime.datetime.now().isoformat(), "hash": sha256(MANIFEST_PATH)}
        json.dump(manifest, open(MANIFEST_PATH, "w"), indent=2)
        log("Manifesto atualizado.")

if __name__ == "__main__":
    main()
