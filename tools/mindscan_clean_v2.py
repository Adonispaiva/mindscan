#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MindScan Factory - Git Cleaner Automation v2.1
Autor: Adonis Paiva (Inovexa Software)
Descrição: Mantém o repositório leve, detecta inflamentos,
faz limpeza total automática, gera log e notifica o Command Center.
"""

import os, subprocess, shutil, time, json, requests
from pathlib import Path
from datetime import datetime

# === CONFIGURAÇÕES ===
REPO_DIR = Path(__file__).resolve().parents[1]
GITIGNORE = REPO_DIR / ".gitignore"
LOG_DIR = REPO_DIR / "mindscan_logs"
LOG_FILE = LOG_DIR / "maintenance.log"
MAX_FILE_SIZE_MB = 100
MAX_REPO_SIZE_MB = 1000
BRANCH = "v2.1-dev"
RETRY_DELAY_SEC = 10
MAX_RETRIES = 3

# Notificação opcional
NOTIFY_ENABLED = True
TELEGRAM_TOKEN = "<SEU_TOKEN_TELEGRAM>"
TELEGRAM_CHAT_ID = "<SEU_CHAT_ID>"

# === UTILITÁRIOS ===
def log(msg: str, level="INFO"):
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def notify_remote(msg: str):
    if NOTIFY_ENABLED and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            log(f"Falha ao enviar notificação: {e}", "WARN")

def run(cmd: str, check=True):
    log(f"→ {cmd}")
    result = subprocess.run(cmd, cwd=REPO_DIR, shell=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.strip():
        log(result.stdout.strip())
    if result.stderr.strip():
        log(result.stderr.strip(), "ERR")
    if check and result.returncode != 0:
        raise RuntimeError(f"Erro ao executar: {cmd}")
    return result

def get_repo_size_mb():
    total = sum(f.stat().st_size for f in REPO_DIR.rglob('*')
                if '.git' not in f.parts)
    return round(total / (1024 * 1024), 2)

def find_large_files(limit_mb=MAX_FILE_SIZE_MB):
    large = []
    for f in REPO_DIR.rglob('*'):
        if f.is_file() and ".git" not in f.parts:
            size = f.stat().st_size / (1024 * 1024)
            if size > limit_mb:
                large.append((size, f))
    for s, p in sorted(large, reverse=True):
        log(f"⚠️ {p.relative_to(REPO_DIR)} → {s:.1f} MB")
    return large

# === FUNÇÕES PRINCIPAIS ===
def update_gitignore():
    ignore_patterns = [
        "backup/", "*.zip", "*.rar", "*.7z", "*.tar", "*.gz",
        "*.mp4", "*.png", "*.jpg", "*.jpeg", "*.webp",
        "*.exe", "*.dll", "*.aab", "*.apk", "__pycache__/",
        "*.env", "*.log", "*.sqlite3"
    ]
    lines = set(GITIGNORE.read_text().splitlines()) if GITIGNORE.exists() else set()
    with open(GITIGNORE, "a", encoding="utf-8") as f:
        for p in ignore_patterns:
            if p not in lines:
                f.write(p + "\n")
    log("✅ .gitignore atualizado.")

def remove_from_git(large_files):
    if not large_files:
        log("Nenhum arquivo acima do limite.")
        return
    for _, path in large_files:
        rel = path.relative_to(REPO_DIR)
        run(f'git rm --cached "{rel}"', check=False)

def clean_history():
    run("git reflog expire --expire=now --all", check=False)
    run("git gc --prune=now --aggressive", check=False)

def reset_git_history():
    """Reinicializa o histórico Git com resiliência e retentativa."""
    log("⚠️ Repositório excedeu limite de tamanho — resetando histórico completo...")

    git_dir = REPO_DIR / ".git"
    for attempt in range(1, MAX_RETRIES + 1):
        if git_dir.exists():
            try:
                run(f'attrib -R /S /D "{git_dir}"', check=False)
                run(f'takeown /F "{git_dir}" /R /D Y', check=False)
                shutil.rmtree(git_dir, ignore_errors=True)
                if git_dir.exists():
                    raise PermissionError("Falha ao remover .git")
            except Exception as e:
                log(f"Tentativa {attempt}: {e}", "WARN")
                if attempt < MAX_RETRIES:
                    log(f"Aguardando {RETRY_DELAY_SEC}s para nova tentativa...")
                    time.sleep(RETRY_DELAY_SEC)
                    continue
                else:
                    notify_remote("❌ Falha persistente ao remover .git.")
                    raise
        break

    run("git init")
    run("git add .")
    run('git commit -m \"Reinitialized clean repository (auto-maintenance)\"')
    run(f"git branch -M {BRANCH}")
    run(f"git remote add origin git@github.com:Adonispaiva/mindscan.git")
    run(f"git push -u origin {BRANCH} --force")
    log("✅ Histórico Git refeito com sucesso.")
    notify_remote("✅ MindScan: histórico Git refeito com sucesso.")

def commit_and_push():
    run('git add .gitignore', check=False)
    msg = f"[auto] Clean run @ {datetime.now():%Y-%m-%d %H:%M:%S}"
    run(f'git commit -m "{msg}"', check=False)
    run(f'git push origin {BRANCH} --force', check=False)
    log("Push finalizado com sucesso.")
    notify_remote("✅ MindScan push concluído.")

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    log(f"🧩 MindScan Factory Git Cleaner v2.1 - {datetime.now():%Y-%m-%d %H:%M:%S}")
    repo_size = get_repo_size_mb()
    log(f"📦 Tamanho atual do repositório: {repo_size} MB")

    try:
        if repo_size > MAX_REPO_SIZE_MB:
            reset_git_history()
        else:
            large_files = find_large_files()
            update_gitignore()
            remove_from_git(large_files)
            clean_history()
            commit_and_push()
        log("🏁 Manutenção concluída com sucesso.")
    except Exception as e:
        log(f"❌ Erro fatal: {e}", "FATAL")
        notify_remote(f"❌ MindScan Factory erro: {e}")
