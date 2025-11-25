import os
import subprocess
import json
import hashlib
import zipfile
from datetime import datetime

# ===============================
# CONFIGURAÇÕES PRINCIPAIS
# ===============================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
AUDITOR_SCRIPT = os.path.join(PROJECT_ROOT, "auditar_mindscan.py")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "backups")
LOG_FILE = os.path.join(PROJECT_ROOT, "log_sincronizacao.txt")
IGNORAR_EXTENSOES = {"pyc", "pyo", "zip", "exe"}
IGNORAR_PASTAS = {"__pycache__", ".git", "venv", "env", "dist", "build", "node_modules"}

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def executar(cmd):
    resultado = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return resultado.stdout.strip(), resultado.stderr.strip()

def registrar_log(texto):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}]\n{texto}\n\n")

def obter_branch_atual():
    stdout, _ = executar("git branch --show-current")
    return stdout if stdout else "main"

def ha_modificacoes_pendentes():
    stdout, _ = executar("git status -s")
    return stdout.strip() != ""

def gerar_hash_global():
    sha = hashlib.sha256()
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
        for file in files:
            ext = file.split(".")[-1]
            if ext in IGNORAR_EXTENSOES:
                continue
            caminho = os.path.join(root, file)
            with open(caminho, "rb") as f:
                sha.update(f.read())
    return sha.hexdigest()

def criar_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    nome_zip = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    caminho_zip = os.path.join(BACKUP_DIR, nome_zip)
    with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [d for d in dirs if d not in IGNORAR_PASTAS]
            for file in files:
                if file.endswith(('.pyc', '.pyo', '.zip')):
                    continue
                caminho_arq = os.path.join(root, file)
                zipf.write(caminho_arq, os.path.relpath(caminho_arq, PROJECT_ROOT))
    return caminho_zip

def executar_auditoria():
    registrar_log("Executando auditoria automática...")
    stdout, stderr = executar(f"python \"{AUDITOR_SCRIPT}\"")
    return stdout, stderr

def commit_automatico():
    if not ha_modificacoes_pendentes():
        return "Nenhuma alteração para commit."
    stdout_status, _ = executar("git status -s")
    mensagem = (
        "Commit automático — "
        + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        + "\nArquivos alterados:\n"
        + stdout_status
    )
    executar("git add .")
    stdout, stderr = executar(f'git commit -m "{mensagem}"')
    if stderr and "nothing to commit" not in stderr:
        return f"Erro no commit: {stderr}"
    return "Commit realizado com sucesso."

def push_automatico(branch):
    stdout, stderr = executar(f"git push origin {branch}")
    if stderr and "Everything up-to-date" not in stderr:
        return f"Erro no push: {stderr}"
    return "Push concluído com sucesso."

def checar_divergencias():
    stdout, stderr = executar("git fetch --dry-run")
    if stdout or stderr:
        return True
    return False

# ===============================
# FLUXO PRINCIPAL
# ===============================
def executar_sincronizacao():
    inicio = f"=== SINCRONIZAÇÃO AVANÇADA — {datetime.now()} ==="
    print(inicio)
    registrar_log(inicio)

    branch = obter_branch_atual()
    print(f"📍 Branch atual: {branch}")
    registrar_log(f"Branch atual detectado: {branch}")

    print("\n📌 Verificando divergências com o remoto...")
    if checar_divergencias():
        alerta = (
            "⚠️ Divergências encontradas entre local e GitHub.\n"
            "O script está em modo SEGURO (sem pull automático).\n"
            "Execute manualmente: git pull origin {branch}\n"
        )
        print(alerta)
        registrar_log(alerta)

    print("\n📌 Gerando backup local...")
    caminho_backup = criar_backup()
    registrar_log(f"Backup criado: {caminho_backup}")

    print("\n📌 Executando auditoria completa do MindScan...")
    aud_stdout, aud_stderr = executar_auditoria()
    registrar_log(aud_stdout)
    if aud_stderr:
        registrar_log("ERRO na auditoria: " + aud_stderr)

    print("\n📌 Gerando hash global do projeto...")
    hash_valor = gerar_hash_global()
    registrar_log(f"Hash global: {hash_valor}")

    print("\n📌 Verificando alterações para commit...")
    msg_commit = commit_automatico()
    print(msg_commit)
    registrar_log(msg_commit)

    print("\n📌 Realizando push...")
    msg_push = push_automatico(branch)
    print(msg_push)
    registrar_log(msg_push)

    final = f"=== FINALIZADO — {datetime.now()} ==="
    print(final)
    registrar_log(final)


if __name__ == "__main__":
    executar_sincronizacao()