# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\instalador_mindscan.py
# Última atualização: 2025-12-11T09:59:20.420850

# instalador_mindscan.py
import os
import shutil
import json
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = "C:/MindScan"
LOG_DIR = os.path.join(ROOT, "logs", "instalador")
VERSION_FILE = os.path.join(INSTALL_DIR, "versao_instalada.json")
TREE_FILE = os.path.join(INSTALL_DIR, "estrutura_instalada.json")

BACKUP_DIR = os.path.join(ROOT, "backups", "instalador")


def log(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    fpath = os.path.join(LOG_DIR, "instalador.log")
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(fpath, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg)


def gerar_arvore(caminho):
    estrutura = []
    for raiz, dirs, files in os.walk(caminho):
        for f in files:
            estrutura.append(os.path.join(raiz, f))
    return estrutura


def backup():
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)
    if os.path.exists(INSTALL_DIR):
        shutil.copytree(INSTALL_DIR, BACKUP_DIR)
        log("📦 Backup criado antes da atualização.")


def rollback():
    if os.path.exists(BACKUP_DIR):
        if os.path.exists(INSTALL_DIR):
            shutil.rmtree(INSTALL_DIR)
        shutil.copytree(BACKUP_DIR, INSTALL_DIR)
        log("⚠ Rollback realizado devido a falha.")


def instalar():
    log("🛠 Iniciando instalador avançado MindScan...")

    backup()

    try:
        if os.path.exists(INSTALL_DIR):
            shutil.rmtree(INSTALL_DIR)

        shutil.copytree(ROOT, INSTALL_DIR, dirs_exist_ok=True)

        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "versao": datetime.datetime.now().isoformat(),
            }, f, indent=4)

        with open(TREE_FILE, "w", encoding="utf-8") as f:
            json.dump(gerar_arvore(INSTALL_DIR), f, indent=4)

        log("✔ Instalação concluída com sucesso!")

    except Exception as e:
        log(f"❌ Erro durante a instalação: {e}")
        rollback()


if __name__ == "__main__":
    instalar()
