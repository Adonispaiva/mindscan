#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MindScan Factory - Git Cleaner Automation
Autor: Adonis Paiva (Inovexa Software)
Descrição: Remove arquivos grandes, limpa histórico e faz push otimizado.
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

# Configurações
REPO_DIR = Path(__file__).resolve().parent
BACKUP_DIR = REPO_DIR / "backup"
GITIGNORE = REPO_DIR / ".gitignore"
MAX_FILE_SIZE_MB = 100
BRANCH = "v2.1-dev"

# Utilitário para execução de comandos shell
def run(cmd: str, check=True):
    print(f"\033[96m→ {cmd}\033[0m")
    result = subprocess.run(cmd, shell=True, cwd=REPO_DIR, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"\033[91m{result.stderr}\033[0m")
    if check and result.returncode != 0:
        raise RuntimeError(f"Erro ao executar: {cmd}")
    return result

# 1️⃣ - Detectar arquivos grandes
def find_large_files(limit_mb=100):
    print(f"\n🔍 Procurando arquivos > {limit_mb} MB...")
    large_files = []
    for root, _, files in os.walk(REPO_DIR):
        for f in files:
            path = Path(root) / f
            if ".git" in path.parts:
                continue
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > limit_mb:
                large_files.append((size_mb, path))
    large_files.sort(reverse=True)
    for s, p in large_files:
        print(f"⚠️  {p.relative_to(REPO_DIR)} → {s:.1f} MB")
    return large_files

# 2️⃣ - Atualizar .gitignore
def update_gitignore():
    ignore_entries = [
        "backup/",
        "*.zip", "*.rar", "*.7z", "*.tar", "*.gz",
        "*.apk", "*.aab", "*.exe", "*.dll", "*.so",
        "*.mp4", "*.png", "*.jpg", "*.jpeg", "*.webp",
    ]
    existing = set()
    if GITIGNORE.exists():
        existing = set(GITIGNORE.read_text().splitlines())

    with GITIGNORE.open("a", encoding="utf-8") as f:
        for entry in ignore_entries:
            if entry not in existing:
                f.write(entry + "\n")

    print("✅ .gitignore atualizado.")

# 3️⃣ - Remover grandes arquivos do Git
def remove_from_git(large_files):
    if not large_files:
        print("✅ Nenhum arquivo acima do limite.")
        return
    print("\n🧹 Removendo arquivos grandes do Git...")
    for _, path in large_files:
        rel = path.relative_to(REPO_DIR)
        try:
            run(f'git rm --cached "{rel}"', check=False)
        except Exception as e:
            print(f"⚠️ Falha ao remover {rel}: {e}")

# 4️⃣ - Compactar e limpar histórico
def clean_git_history():
    print("\n🧠 Limpando histórico Git...")
    run("git reflog expire --expire=now --all", check=False)
    run("git gc --prune=now --aggressive", check=False)

# 5️⃣ - Commitar e enviar
def commit_and_push():
    print("\n🚀 Commitando e enviando alterações...")
    run('git add .gitignore', check=False)
    msg = f"[auto] Clean large files @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run(f'git commit -m "{msg}"', check=False)
    run(f'git push origin {BRANCH} --force', check=False)
    print("\n✅ Push finalizado com sucesso!")

# Execução principal
if __name__ == "__main__":
    print(f"\n🧩 MindScan Factory Git Cleaner - {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 60)

    large_files = find_large_files(MAX_FILE_SIZE_MB)
    update_gitignore()
    remove_from_git(large_files)
    clean_git_history()
    commit_and_push()

    print("\n🏁 Processo concluído com sucesso!")
