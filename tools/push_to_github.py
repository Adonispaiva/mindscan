# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\push_to_github.py
# Última atualização: 2025-12-11T09:59:27.808460

import os
import subprocess
import datetime
import json
import sys
from pathlib import Path
import hashlib

# ============================================================
#  MindScan — Kernel Git Enterprise
#  Push Inteligente com Auditoria, Logs, Diferenças Reais,
#  Anti-Commit Gigante, Verificação de Timestamps
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / ".mindscan_push.log"


# ---------------------- UTILITÁRIOS -------------------------

def log_event(event_type, data):
    """Grava eventos estruturados no log do MindScan."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event_type,
        "data": data,
    }
    LOG_FILE.write_text(
        (LOG_FILE.read_text() if LOG_FILE.exists() else "") +
        json.dumps(entry, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )


def run(cmd):
    """Executa comandos git e retorna stdout/stderr."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True
    )
    return result.stdout.strip(), result.stderr.strip()


def get_changed_files():
    """Lista arquivos modificados, adicionados ou removidos."""
    out, _ = run("git status --porcelain")
    changed = []
    for line in out.splitlines():
        status = line[:2].strip()
        path = line[3:].strip()
        changed.append((status, path))
    return changed


def file_size(path):
    p = PROJECT_ROOT / path
    return p.stat().st_size if p.exists() else 0


def scan_ghost_directories():
    """Detecta diretórios que não mudam mas aparecem como defasados."""
    ghost = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if ".git" in root:
            continue
        last_mod = max(
            ((Path(root)/f).stat().st_mtime for f in files),
            default=None
        )
        if last_mod is None:
            continue

        age_minutes = (datetime.datetime.now().timestamp() - last_mod) / 60
        if age_minutes > 1440:  # 24h
            ghost.append(root.replace(str(PROJECT_ROOT), "").strip("\\/"))

    return ghost


def validate_commit_volume(changed):
    """Impede commits gigantes ou suspeitos."""
    total_size = sum(file_size(p) for (_, p) in changed)
    if total_size > 20_000_000:  # 20MB
        return False, total_size
    for (_, p) in changed:
        if file_size(p) > 5_000_000:  # 5MB individual
            return False, p
    return True, None


def verify_timestamp_integrity():
    """Verifica divergências > 5 minutos entre arquivos alterados."""
    issues = []
    now = datetime.datetime.now().timestamp()

    for root, dirs, files in os.walk(PROJECT_ROOT):
        if ".git" in root:
            continue
        for f in files:
            p = Path(root) / f
            m = p.stat().st_mtime
            if abs(now - m) > 300:
                issues.append(str(p).replace(str(PROJECT_ROOT), ""))

    return issues


# ---------------------- PIPELINE ----------------------------

def main():
    print("\n=== MindScan — Pipeline Enterprise de Push ===\n")
    log_event("start", {"message": "Pipeline iniciado"})

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("[ERRO] GITHUB_TOKEN não configurado.")
        log_event("error", {"missing_token": True})
        sys.exit(1)

    remote_url = f"https://{token}:x-oauth-basic@github.com/Adonispaiva/mindscan.git"

    print("[1/8] Ajustando remote seguro…")
    _, err = run(f'git remote set-url origin {remote_url}')
    if err:
        log_event("warn", {"remote_set_url": err})

    print("[2/8] Verificando mudanças reais…")
    changed = get_changed_files()
    log_event("changed_files", {"count": len(changed), "files": changed})

    if not changed:
        print("Nenhuma mudança real. Push abortado.")
        log_event("abort", {"reason": "no_changes"})
        sys.exit(0)

    print("[3/8] Detectando diretórios fantasma…")
    ghosts = scan_ghost_directories()
    log_event("ghost_directories", ghosts)

    print("[4/8] Verificando volume do commit…")
    ok, info = validate_commit_volume(changed)
    if not ok:
        print("❌ Commit gigante detectado! Push bloqueado.")
        log_event("abort_giant_commit", {"info": info})
        sys.exit(1)

    print("[5/8] Inspecionando integridade de timestamps…")
    ts_issues = verify_timestamp_integrity()
    if ts_issues:
        print("⚠️ Divergências de timestamp detectadas.")
        log_event("timestamp_issues", ts_issues)

    print("[6/8] Adicionando arquivos…")
    out, err = run("git add .")
    if err:
        log_event("warn", {"git_add": err})

    msg = f"MindScan — Push Enterprise — {datetime.datetime.now()}"
    print("[7/8] Realizando commit…")
    _, err = run(f'git commit -m "{msg}"')
    if "nothing to commit" in err.lower():
        print("Nenhuma alteração. Push cancelado.")
        log_event("abort", {"reason": "nothing_to_commit"})
        sys.exit(0)

    print("[8/8] Enviando push…")
    out, err = run("git push origin main")
    if err:
        print("❌ Erro no push.")
        log_event("error_push", {"stderr": err})
        sys.exit(1)

    print("\n✓ Push concluído com sucesso!")
    log_event("success", {"message": "Push finalizado com sucesso"})


if __name__ == "__main__":
    main()
