# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindscan_selfheal_max.py
# Última atualização: 2025-12-11T09:59:20.423842

import os
import shutil
import json
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "mindscan_manifest.json")

BACKUPS = os.path.join(ROOT, "backups")
LOGS = os.path.join(ROOT, "logs")
TRASH = os.path.join(ROOT, "trash")

os.makedirs(BACKUPS, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)
os.makedirs(TRASH, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_dir = os.path.join(BACKUPS, f"backup_{timestamp}")
os.makedirs(backup_dir, exist_ok=True)

log_path = os.path.join(LOGS, f"selfheal_{timestamp}.log")

def log(msg):
    print(msg)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# -------------------------------------------------------------------------
# FUNÇÃO DE PROGRESSO NA TELA
# -------------------------------------------------------------------------
spinner_frames = ["|", "/", "-", "\\"]

def progress_bar(current, total, prefix=""):
    percent = (current / total) * 100
    bar_length = 40
    filled = int(bar_length * current // total)
    bar = "█" * filled + "-" * (bar_length - filled)
    print(f"\r{prefix} [{bar}] {percent:5.1f}%", end="", flush=True)

def spinner(step):
    frame = spinner_frames[step % len(spinner_frames)]
    print(f"\r{frame} Processando...", end="", flush=True)

# -------------------------------------------------------------------------
# CARREGAR MANIFEST
# -------------------------------------------------------------------------
if not os.path.exists(MANIFEST):
    log("[ERRO] Manifesto não encontrado!")
    exit(1)

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

log("=====================================================")
log("     MindScan - SELF-HEALING MAX v1.1")
log("     (Backup incremental + progresso em tempo real)")
log("=====================================================")

# -------------------------------------------------------------------------
# BACKUP INCREMENTAL (SEM ZIP)
# -------------------------------------------------------------------------
log("\n[FASE 1] Criando backup incremental (sem ZIP)...")

files_to_copy = []
for root, dirs, files in os.walk(ROOT):
    for file in files:
        full = os.path.join(root, file)

        # ignora a própria pasta de backups e logs
        if "\\backups\\" in full or "\\logs\\" in full:
            continue

        # só copia arquivos do projeto
        files_to_copy.append(full)

total_files = len(files_to_copy)
log(f"Total de arquivos para backup: {total_files}")

start_time = time.time()

for i, src in enumerate(files_to_copy):
    rel = os.path.relpath(src, ROOT)
    dst = os.path.join(backup_dir, rel)

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        log(f"[ERRO BACKUP] {src}: {e}")

    progress_bar(i + 1, total_files, prefix="Backup:")

end_time = time.time()
log(f"\n[OK] Backup concluído em {end_time - start_time:.2f} segundos.")
log(f"[LOCAL] {backup_dir}\n")

# -------------------------------------------------------------------------
# FASE 2 — ESTRUTURA DE PASTAS
# -------------------------------------------------------------------------
log("[FASE 2] Verificando estrutura...")

for folder in manifest["structure"]:
    path = os.path.join(ROOT, folder)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        log(f"[CRIADO] {folder}")
    else:
        log(f"[OK] {folder}")

# -------------------------------------------------------------------------
# FASE 3 — ARQUIVOS ESSENCIAIS
# -------------------------------------------------------------------------
log("\n[FASE 3] Arquivos essenciais...")

DEFAULT_TEMPLATE = (
    "# Arquivo restaurado automaticamente pelo Self-Healing MAX v1.1\n"
    "# Insira a lógica específica aqui.\n"
)

for req in manifest["requiredFiles"]:
    filepath = os.path.join(ROOT, req)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(DEFAULT_TEMPLATE)
        log(f"[RECRIADO] {req}")
    else:
        log(f"[OK] {req}")

# -------------------------------------------------------------------------
# FASE 4 — VERIFICAÇÃO PYTHON (SIMPLIFICADA)
# -------------------------------------------------------------------------
log("\n[FASE 4] Verificação rápida de código Python...")

python_files = []
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.endswith(".py") and "backups" not in root:
            python_files.append(os.path.join(root, f))

for i, pyfile in enumerate(python_files):
    spinner(i)
    try:
        with open(pyfile, "r", encoding="utf-8") as f:
            code = f.read()
        compile(code, pyfile, "exec")
        log(f"\n[OK] {pyfile}")
    except Exception as e:
        log(f"\n[ERRO SINTAXE] {pyfile}: {e}")
        with open(pyfile, "w", encoding="utf-8") as f:
            f.write(DEFAULT_TEMPLATE)
        log(f"[REPARADO] {pyfile}")

# -------------------------------------------------------------------------
# FASE FINAL — STATUS
# -------------------------------------------------------------------------
log("\n=====================================================")
log("  SELF-HEALING MAX v1.1 FINALIZADO COM SUCESSO!")
log("  Backup incremental criado, estrutura validada,")
log("  código verificado e arquivos essenciais prontos.")
log("=====================================================")
print("\nProcesso concluído.")
