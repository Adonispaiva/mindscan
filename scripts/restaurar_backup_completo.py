import os
import shutil
import subprocess
import zipfile
import datetime

# === CONFIGURAÇÕES GERAIS ===
RCLONE_REMOTE = "mindscan-drive"
BACKUP_DIR_REMOTE = "backups"
RESTORE_DIR = "../backup_restore"
PROJETO_DIR = "../projetos-inovexa/mindscan"
VENV_ACTIVATE_SCRIPT = os.path.join(PROJETO_DIR, ".venv", "Scripts", "activate")

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def validar_dependencias():
    try:
        subprocess.run(["rclone", "--version"], check=True, stdout=subprocess.DEVNULL)
        log("✅ rclone encontrado.")
    except subprocess.CalledProcessError:
        raise RuntimeError("❌ rclone não está instalado ou configurado corretamente.")

def obter_backup_mais_recente():
    log("🔍 Buscando o backup mais recente no Google Drive...")
    result = subprocess.check_output([
        "rclone", "lsjson", f"{RCLONE_REMOTE}:{BACKUP_DIR_REMOTE}"
    ]).decode("utf-8")

    import json
    arquivos = json.loads(result)
    backups_zip = [
        f for f in arquivos
        if f["Name"].endswith(".zip")
    ]
    if not backups_zip:
        raise FileNotFoundError("❌ Nenhum arquivo .zip de backup encontrado no Google Drive.")

    mais_recente = max(backups_zip, key=lambda f: f["ModTime"])
    nome = mais_recente["Name"]
    log(f"📦 Backup mais recente: {nome}")
    return nome

def baixar_backup(nome_arquivo):
    os.makedirs(RESTORE_DIR, exist_ok=True)
    destino = os.path.join(RESTORE_DIR, nome_arquivo)

    if os.path.exists(destino):
        log(f"ℹ️ Arquivo já baixado: {destino}")
        return destino

    log("⬇️ Baixando backup...")
    subprocess.run([
        "rclone", "copy", f"{RCLONE_REMOTE}:{BACKUP_DIR_REMOTE}/{nome_arquivo}",
        RESTORE_DIR, "--progress"
    ], check=True)
    log("✅ Download concluído.")
    return destino

def extrair_backup(caminho_zip):
    log(f"📂 Extraindo backup em: {RESTORE_DIR}")
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        zip_ref.extractall(PROJETO_DIR)
    log("✅ Extração concluída.")

def restaurar_ambiente_virtual():
    activate = os.path.join(PROJETO_DIR, ".venv", "Scripts", "activate")
    requirements = os.path.join(PROJETO_DIR, "requirements.txt")

    if not os.path.exists(requirements):
        log("⚠️ Nenhum arquivo requirements.txt encontrado. Pulando instalação de dependências.")
        return

    log("📦 Instalando dependências no ambiente virtual...")
    subprocess.run([
        os.path.join(PROJETO_DIR, ".venv", "Scripts", "pip"), "install", "-r", requirements
    ], check=True)
    log("✅ Dependências instaladas.")

def restaurar_banco_de_dados():
    # TODO: Implementar restauração do banco se aplicável (ex: SQLite, PostgreSQL)
    log("🗄️ Restauração do banco de dados: ainda não implementado (nenhuma instrução encontrada).")

def main():
    try:
        validar_dependencias()
        nome_backup = obter_backup_mais_recente()
        zip_path = baixar_backup(nome_backup)
        extrair_backup(zip_path)
        restaurar_ambiente_virtual()
        restaurar_banco_de_dados()
        log("🏁 Projeto restaurado com sucesso!")
    except Exception as e:
        log(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
