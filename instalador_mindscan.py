import os
import shutil
import subprocess
from datetime import datetime

# Instalador Automático MindScan
# Copia arquivos essenciais, cria ambientes e gera scripts auxiliares

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
INSTALL_DIR = "C:/MindScan"  # Caminho final da instalação
BACKUP_DIR = os.path.join(INSTALL_DIR, "backup_instalador")


def criar_diretorios():
    os.makedirs(INSTALL_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)


def copiar_arquivos():
    for item in os.listdir(PROJECT_ROOT):
        origem = os.path.join(PROJECT_ROOT, item)
        destino = os.path.join(INSTALL_DIR, item)
        if item in {"__pycache__", "venv", "env", "build", "dist"}:
            continue
        if os.path.isdir(origem):
            shutil.copytree(origem, destino, dirs_exist_ok=True)
        else:
            shutil.copy2(origem, destino)


def criar_backup():
    arquivo = os.path.join(BACKUP_DIR, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
    shutil.make_archive(arquivo.replace('.zip', ''), 'zip', INSTALL_DIR)


def criar_launcher():
    launcher_path = os.path.join(INSTALL_DIR, "executar_mindscan.bat")
    with open(launcher_path, "w") as f:
        f.write(f"@echo off\n")
        f.write(f"cd /d {INSTALL_DIR}\n")
        f.write(f"python main.py\n")


def instalar_dependencias():
    req_path = os.path.join(INSTALL_DIR, "requirements.txt")
    if os.path.exists(req_path):
        subprocess.run(["pip", "install", "-r", req_path])


def executar_instalacao():
    print("Iniciando instalador automático MindScan...")
    criar_diretorios()
    copiar_arquivos()
    criar_backup()
    criar_launcher()
    instalar_dependencias()
    print("Instalação concluída com sucesso!")


if __name__ == "__main__":
    executar_instalacao()
