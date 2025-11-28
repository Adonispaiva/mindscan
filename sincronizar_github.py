import os
import subprocess
import hashlib
import json
import datetime
import threading

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# ------------------------------------------------------------
# UTIL
# ------------------------------------------------------------
def sha256_file(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def executar(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    out, err = proc.communicate()
    return out.strip() if out else "", err.strip() if err else ""


# ------------------------------------------------------------
# AUDITORIA MAX
# ------------------------------------------------------------
def auditoria_max():
    print("🔍 Iniciando Auditoria MAX...")

    resultado = {
        "timestamp": str(datetime.datetime.now()),
        "arquivos": [],
        "alertas": []
    }

    for raiz, _, arquivos in os.walk(ROOT):
        for arq in arquivos:
            caminho = os.path.join(raiz, arq)

            if ".git" in caminho:
                continue

            info = {
                "arquivo": caminho.replace(ROOT, ""),
                "size": os.path.getsize(caminho),
                "modified": datetime.datetime.fromtimestamp(os.path.getmtime(caminho)).isoformat(),
                "sha256": sha256_file(caminho)
            }
            resultado["arquivos"].append(info)

    # Salva JSON
    json_path = os.path.join(LOG_DIR, "auditoria_MAX.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print("✔ Auditoria MAX finalizada.")
    return json_path


# ------------------------------------------------------------
# GIT: STATUS, ADD, COMMIT, PULL, PUSH
# ------------------------------------------------------------
def sincronizar():
    print("🌐 Sincronizando com GitHub...")

    executar(f"git -C \"{ROOT}\" add .")

    msg = f"Auditoria e push automáticos ({datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')})"
    executar(f"git -C \"{ROOT}\" commit -m \"{msg}\"")

    executar(f"git -C \"{ROOT}\" pull --no-edit")
    executar(f"git -C \"{ROOT}\" push")

    print("✔ Sincronização concluída.")


# ------------------------------------------------------------
# PIPELINE FINAL
# ------------------------------------------------------------
def executar_pipeline():
    print("=========================================")
    print("      🚀 Sincronização Completa – INÍCIO")
    print("=========================================")

    auditoria_max()
    sincronizar()

    print("=========================================")
    print("           ✔ PIPELINE CONCLUÍDO")
    print("=========================================")


if __name__ == "__main__":
    executar_pipeline()
