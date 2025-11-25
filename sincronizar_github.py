#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import json
import datetime
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "log_sincronizacao.txt")
BACKUP_DIR = os.path.join(ROOT, "backups", "git_state")
AUDITOR_SCRIPT = os.path.join(ROOT, "auditar_mindscan.py")

BRANCH = "main"
REMOTE = "origin"
REMOTE_URL = "https://github.com/Adonispaiva/mindscan.git"


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg)


def executar(cmd):
    """Executa comando com tolerância a erros e encoding corrigido."""
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="ignore"
    )
    out, err = proc.communicate()
    return out.strip() if out else "", err.strip() if err else ""


def backup_estado():
    """Copia o .git inteiro para um backup local."""
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)

    src = os.path.join(ROOT, ".git")
    if os.path.exists(src):
        shutil.copytree(src, BACKUP_DIR)
        log("📦 Backup do estado atual do repositório criado.")


def rollback():
    """Restaura o .git caso falhe o push."""
    if os.path.exists(BACKUP_DIR):
        dest = os.path.join(ROOT, ".git")
        shutil.rmtree(dest)
        shutil.copytree(BACKUP_DIR, dest)
        log("⚠️ Rollback realizado: estado do repositório revertido.")
    else:
        log("⚠️ Rollback solicitado, mas não existe backup.")


def configurar_remote():
    """Garante que o remote está configurado corretamente."""
    out, _ = executar("git remote -v")

    if REMOTE_URL not in out:
        log("🔧 Remote incorreto. Ajustando...")
        executar(f"git remote remove {REMOTE}")
        executar(f"git remote add {REMOTE} {REMOTE_URL}")
        log(f"✔ Remote configurado: {REMOTE_URL}")
    else:
        log("✔ Remote já está correto.")


def detectar_modificacoes():
    out, _ = executar("git status --porcelain")
    if out.strip():
        return True, out
    return False, ""


def executar_auditoria():
    """Executa auditoria completa antes do push."""
    if not os.path.exists(AUDITOR_SCRIPT):
        log("⚠ Auditor não encontrado, ignorando auditoria pré-push.")
        return

    log("📊 Executando auditoria completa do MindScan...")
    out, err = executar(f"python \"{AUDITOR_SCRIPT}\"")
    if err:
        log(f"⚠ Auditoria gerou erros: {err}")
    else:
        log("✔ Auditoria finalizada.")


def sincronizar():
    log("\n==========================================================")
    log("🔁 SINCRONIZAÇÃO AVANÇADA DO MINDSCAN — INÍCIO")
    log("==========================================================\n")

    configurar_remote()

    # backup
    backup_estado()

    # git fetch
    executar("git fetch origin")

    # detectar mudanças locais
    mudou, detalhes = detectar_modificacoes()

    if mudou:
        log("📝 Detalhes das mudanças locais:\n" + detalhes)

        log("📌 Adicionando arquivos ao stage...")
        executar("git add .")

        mensagem = f"Atualização automática — {datetime.datetime.now()}"
        executar(f"git commit -m \"{mensagem}\"")
        log("✔ Commit criado.")
    else:
        log("Nenhuma modificação local detectada.")

    executar_auditoria()

    # push
    log("⬆️ Enviando alterações ao GitHub...")
    out, err = executar(f"git push -u origin {BRANCH}")

    if "error" in err.lower():
        log("❌ Erro ao enviar para o GitHub:")
        log(err)
        rollback()
    else:
        log("✔ Código sincronizado com sucesso!")

    log("==========================================================")
    log("✔ SINCRONIZAÇÃO FINALIZADA")
    log("==========================================================\n")


if __name__ == "__main__":
    sincronizar()
