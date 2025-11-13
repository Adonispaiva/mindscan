# ============================================================
# Inovexa Fábrica — Push Automático MindScan v4.1-Stable
# ============================================================
# Autor: Leo Vinci | Diretor de Tecnologia & Produção Inovexa
# Build: 2025-11-10 | Compatível: Windows 10+ / Python >= 3.10
# ------------------------------------------------------------
# Funções principais:
#  • Backup completo com exclusões automáticas
#  • Commit + Push automático (via Token HTTPS)
#  • Autodiagnóstico de encoding e ambiente
#  • Logger resiliente com retry em caso de lock
#  • Anti-push redundante (HEAD tracking)
#  • Relatório HTML e Manifesto JSON
# ============================================================

import os
import sys
import subprocess
import datetime
import hashlib
import json
import zipfile
import time
import locale
import platform
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# CONFIGURAÇÃO GERAL
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"
BACKUP_DIR = BASE_DIR / "backup"
BACKUP_DIR.mkdir(exist_ok=True)

LOG_PATH = BACKUP_DIR / "push_runtime.log"
HASH_FILE = BACKUP_DIR / "last_push_hash.txt"

# ============================================================
# DETECÇÃO DE ENCODING
# ============================================================
def configure_console_encoding():
    """Detecta e ajusta o encoding do console dinamicamente."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        encoding = "utf-8"
    except Exception:
        fallback = locale.getpreferredencoding(False)
        sys.stdout.reconfigure(encoding=fallback)
        encoding = fallback
    print(f"[INFO] Console encoding: {encoding}")
    return encoding

ENCODING_MODE = configure_console_encoding()
OS_INFO = f"{platform.system()} {platform.release()} ({platform.version()})"

# ============================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================
def log_line(message: str):
    """Grava linha no log com retry automático em caso de lock."""
    for attempt in range(3):
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as log:
                log.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {message}\n")
            return
        except PermissionError:
            time.sleep(0.2)
    alt = BACKUP_DIR / f"push_runtime_{int(time.time())}.log"
    with open(alt, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {message}\n")

def run(cmd):
    """Executa comando e retorna stdout, stderr, code."""
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def sha256sum(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for blk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(blk)
    return h.hexdigest()

# ============================================================
# CARREGAR VARIÁVEIS DO .ENV
# ============================================================
load_dotenv(ENV_PATH)
GITHUB_TOKEN  = os.getenv("GITHUB_TOKEN")
GITHUB_USER   = os.getenv("GITHUB_USER")
GITHUB_REPO   = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH")

if not all([GITHUB_TOKEN, GITHUB_USER, GITHUB_REPO, GITHUB_BRANCH]):
    raise EnvironmentError("❌ Variáveis GITHUB_* ausentes no arquivo .env.")

TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ZIP_NAME = f"mindscan_backup_{TS}.zip"
ZIP_PATH = BACKUP_DIR / ZIP_NAME

# ============================================================
# BACKUP SEGURO
# ============================================================
EXCLUDE_DIRS = {"backup", "__pycache__", ".git", ".idea", ".vscode", "venv", ".venv", "node_modules"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".log"}

def safe_backup(src: Path, dest: Path):
    """Gera um backup completo e válido, ignorando pastas indesejadas."""
    print("[INFO] Criando backup do projeto...")
    log_line("Iniciando backup completo...")
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src):
            root_path = Path(root)
            if any(ex in root_path.parts for ex in EXCLUDE_DIRS):
                continue
            for f in files:
                file_path = root_path / f
                if file_path.suffix in EXCLUDE_EXTS:
                    continue
                if BACKUP_DIR in file_path.parents:
                    continue
                arc = file_path.relative_to(src)
                zipf.write(file_path, arc.as_posix())
    log_line(f"Backup criado com sucesso: {dest.name}")

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================
print("\n============================================================")
print("Inovexa Fábrica — Push Automático MindScan v4.1-Stable")
print(f"Sistema: {OS_INFO}")
print(f"Encoding ativo: {ENCODING_MODE}")
print("============================================================\n")

safe_backup(BASE_DIR, ZIP_PATH)
checksum_zip = sha256sum(ZIP_PATH)
print(f"[OK] Backup: {ZIP_PATH.name}")
print(f"[OK] SHA256: {checksum_zip}")

# --- Verificar branch ---
branch, _, _ = run(["git", "-C", str(BASE_DIR), "rev-parse", "--abbrev-ref", "HEAD"])
if branch != GITHUB_BRANCH:
    raise RuntimeError(f"❌ Branch incorreta: {branch} (esperado: {GITHUB_BRANCH})")
print(f"[OK] Branch ativa: {branch}")

# --- Redundância HEAD ---
head_hash, _, _ = run(["git", "-C", str(BASE_DIR), "rev-parse", "HEAD"])
if HASH_FILE.exists() and HASH_FILE.read_text().strip() == head_hash:
    print("[INFO] Nenhuma alteração detectada desde o último push. Encerrando.")
    log_line("Push ignorado — HEAD inalterado.")
    sys.exit(0)

# --- Commit e Push ---
run(["git", "-C", str(BASE_DIR), "add", "."])
run(["git", "-C", str(BASE_DIR), "commit", "-m", f"Automated push - Inovexa MindScan [{TS}]"])
print("[OK] Commit automático criado.")

repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{GITHUB_REPO}.git"
print("[INFO] Executando push remoto...")
out, err, code = run(["git", "-C", str(BASE_DIR), "push", repo_url, GITHUB_BRANCH, "--force"])
status = "SUCESSO" if code == 0 else "FALHA"
print(f"[RESULT] Push: {status}")
if code != 0:
    print(err)
log_line(f"Push: {status} | HEAD={head_hash}")

# --- Manifesto JSON ---
manifest = {
    "timestamp": TS,
    "repository": GITHUB_REPO,
    "branch": GITHUB_BRANCH,
    "status": status,
    "zip_backup": ZIP_NAME,
    "zip_checksum": checksum_zip,
    "git_head": head_hash,
    "encoding_mode": ENCODING_MODE,
    "os_info": OS_INFO,
    "stdout_tail": out[-500:],
    "stderr_tail": err[-500:],
}
manifest_path = BACKUP_DIR / f"manifest_push_{TS}.json"
manifest_path.write_text(json.dumps(manifest, indent=4), encoding="utf-8")
print(f"[OK] Manifesto salvo: {manifest_path.name}")

# --- Relatório HTML ---
template = BACKUP_DIR / "manifest_push_template.html"
html_out = BACKUP_DIR / f"manifest_push_{TS}.html"
html = (
    template.read_text(encoding="utf-8") if template.exists()
    else "<html><body><h2>Relatório Inovexa</h2><p>Status: {{status}}</p></body></html>"
)
html = (
    html.replace("{{timestamp}}", TS)
        .replace("{{repository}}", GITHUB_REPO)
        .replace("{{branch}}", GITHUB_BRANCH)
        .replace("{{status}}", status)
        .replace("{{backup_zip}}", ZIP_NAME)
        .replace("{{checksum}}", checksum_zip)
        .replace("{{log_content}}", (out + "\n" + err if err else out))
)
html_out.write_text(html, encoding="utf-8")
HASH_FILE.write_text(head_hash, encoding="utf-8")

print(f"[OK] Relatório HTML gerado: {html_out.name}")
log_line(f"Relatório HTML: {html_out.name}")

print("\n🏁 Processo concluído com sucesso.")
log_line("=== Execução finalizada sem erros ===")
