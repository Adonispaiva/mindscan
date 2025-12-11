# ================================================================
#  MINDSCAN OPTIMIZER (v2.3 - ENTERPRISE EDITION)
#  Diretor Técnico: Leo Vinci — Inovexa Software
#  Arquivo: mindscan_optimizer.py
#  Local: D:\projetos-inovexa\mindscan\tools\
# ================================================================

import os
import sys
import json
import shutil
import datetime
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
LOGS = TOOLS / "_optimizer_logs"
CHECKPOINTS = ROOT / "_optimizer_checkpoints"
STRUCTURE_LOGS = ROOT / "logs" / "estrutura"

TREE_JSON = ROOT / "full_tree.json"
TREE_TXT = ROOT / "full_tree.txt"

IGNORE_DIRS_TREE = {
    ".git",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "venv",
    ".venv",
    "_optimizer_logs",
    "_optimizer_checkpoints",
    "node_modules",
}

# ----------------------------------------------------------------------
# LOG FUNCTION
# ----------------------------------------------------------------------
def log(msg: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGS / "optimizer.log", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg)

# ----------------------------------------------------------------------
# CLEAN
# ----------------------------------------------------------------------
def perform_clean() -> None:
    log("→ Executando limpeza profunda (CLEAN)…")
    patterns = {"__pycache__", ".pytest_cache", ".DS_Store", "Thumbs.db"}
    for root, dirs, files in os.walk(ROOT):
        for d in list(dirs):
            if d in patterns:
                shutil.rmtree(Path(root) / d, ignore_errors=True)
        for f in list(files):
            if f in patterns:
                try:
                    (Path(root) / f).unlink()
                except:
                    pass
    log("✓ Limpeza concluída.\n")

# ----------------------------------------------------------------------
# NORMALIZE PYTHON
# ----------------------------------------------------------------------
def normalize_python() -> None:
    log("→ Normalizando arquivos Python (NORMALIZE)…")
    for root, _, files in os.walk(ROOT):
        for file in files:
            if not file.endswith(".py"):
                continue
            p = Path(root) / file
            try:
                text = p.read_text(encoding="utf-8")
            except:
                continue
            new = text.replace("\t", "    ")
            if new != text:
                p.write_text(new, encoding="utf-8")
                log(f"  - Normalizado: {p}")
    log("✓ Normalização concluída.\n")

# ----------------------------------------------------------------------
# AUDIT
# ----------------------------------------------------------------------
def checksum_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def perform_audit() -> None:
    log("→ Executando auditoria (AUDIT)…")
    report = {}
    for root, _, files in os.walk(ROOT):
        for f in files:
            p = Path(root) / f
            try:
                report[str(p)] = {
                    "bytes": p.stat().st_size,
                    "checksum": checksum_file(p),
                }
            except:
                pass
    with open(ROOT / "relatorio_auditoria.json", "w", encoding="utf-8") as fp:
        json.dump(report, fp, indent=4)
    log("✓ Auditoria concluída.\n")

# ----------------------------------------------------------------------
# STATS
# ----------------------------------------------------------------------
def compute_stats():
    log("→ Calculando estatísticas (STATS)…")
    total_files = 0
    total_bytes = 0
    for root, _, files in os.walk(ROOT):
        for f in files:
            p = Path(root) / f
            try:
                total_files += 1
                total_bytes += p.stat().st_size
            except:
                pass
    stats = {
        "total_files": total_files,
        "total_bytes": total_bytes,
        "generated_at": datetime.datetime.now().isoformat(),
    }
    with open(ROOT / "stats.json", "w", encoding="utf-8") as fp:
        json.dump(stats, fp, indent=4)
    log("✓ Estatísticas concluídas.\n")

# ----------------------------------------------------------------------
# BASELINE
# ----------------------------------------------------------------------
def update_baseline():
    log("→ Atualizando baseline (BASELINE)…")
    CHECKPOINTS.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = CHECKPOINTS / f"baseline_{now}.json"
    structure = _build_structure()
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(structure, fp, indent=4)
    log(f"✓ Baseline salva em {path}\n")

# ----------------------------------------------------------------------
# FIXES
# ----------------------------------------------------------------------
def apply_fixes():
    log("→ Aplicando correções (FIXES)…")
    placeholder = ROOT / "backend" / "db" / "vazio.md"
    if placeholder.exists():
        log("  - Placeholder DB reconhecido")
    log("✓ Fixes concluídos.\n")

# ----------------------------------------------------------------------
# GOVERNANCE
# ----------------------------------------------------------------------
def generate_governance():
    log("→ Gerando governança (GOVERNANCE)…")
    gov = {
        "generated_at": datetime.datetime.now().isoformat(),
        "optimizer_hash": checksum_file(Path(__file__)),
        "tree_hash": checksum_file(TREE_JSON) if TREE_JSON.exists() else None,
    }
    with open(ROOT / "governance_metadata.json", "w", encoding="utf-8") as fp:
        json.dump(gov, fp, indent=4)
    log("✓ Governança concluída.\n")

# ----------------------------------------------------------------------
# FULLTREE (modo 9)
# ----------------------------------------------------------------------
def _build_structure() -> dict:
    structure = {}
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS_TREE]
        rel = Path(root).resolve().relative_to(ROOT)
        key = "." if str(rel) == "." else str(rel).replace(os.sep, "\\")
        entry = {
            "dirs": sorted(dirs),
            "files": sorted(files),
            "file_info": {},
        }
        for f in entry["files"]:
            p = Path(root) / f
            try:
                entry["file_info"][f] = p.stat().st_size
            except:
                entry["file_info"][f] = None
        structure[key] = entry
    return structure

def _render_text_tree(struct):
    lines = []
    keys = ["."]
    keys.extend(sorted(k for k in struct if k != "."))
    for key in keys:
        entry = struct[key]
        lines.append(f"[{key}]")
        if not entry["dirs"] and not entry["files"]:
            lines.append("  (SEM ARQUIVOS)")
        else:
            for d in entry["dirs"]:
                lines.append(f"  DIR  - {d}")
            for f in entry["files"]:
                size = entry["file_info"].get(f)
                if size == 0:
                    s = " (VAZIO)"
                elif size is None:
                    s = ""
                else:
                    s = f" ({size} bytes)"
                lines.append(f"  FILE - {f}{s}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def generate_tree():
    log("→ FULLTREE (modo 9)…")
    STRUCTURE_LOGS.mkdir(parents=True, exist_ok=True)
    struct = _build_structure()
    TREE_JSON.write_text(json.dumps(struct, indent=4), encoding="utf-8")
    text = _render_text_tree(struct)
    TREE_TXT.write_text(text, encoding="utf-8")
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mmin%Ss")
    (STRUCTURE_LOGS / f"tree_{ts}.txt").write_text(text, encoding="utf-8")
    log("✓ FULLTREE concluído.\n")

# ----------------------------------------------------------------------
# TREE_LEGACY (modo 10)
# ----------------------------------------------------------------------
def _render_ascii_tree():
    """
    Renderização clássica ASCII idêntica ao modelo de 10/12.
    """
    lines = []

    def walk(path: Path, prefix=""):
        items = []
        for p in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            if p.name in IGNORE_DIRS_TREE:
                continue
            items.append(p)
        count = len(items)

        for i, p in enumerate(items):
            is_last = (i == count - 1)
            connector = "└── " if is_last else "├── "
            line = prefix + connector + p.name

            if p.is_file():
                try:
                    size = p.stat().st_size
                    line += f" ({size} bytes)"
                except:
                    pass
                lines.append(line)

            else:
                lines.append(line + "/")
                new_prefix = prefix + ("    " if is_last else "│   ")
                walk(p, new_prefix)

    walk(ROOT)
    return "\n".join(lines)

def generate_tree_legacy():
    log("→ Gerando TREE_LEGACY (modo 10)…")
    STRUCTURE_LOGS.mkdir(parents=True, exist_ok=True)

    text = _render_ascii_tree()

    ts = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mmin%Ss")

    file_tools = TOOLS / f"tree_legacy_{ts}.txt"
    file_logs = STRUCTURE_LOGS / f"tree_legacy_{ts}.txt"

    file_tools.write_text(text, encoding="utf-8")
    file_logs.write_text(text, encoding="utf-8")

    log(f"✓ TREE_LEGACY salvo em:")
    log(f"  - {file_tools}")
    log(f"  - {file_logs}\n")

# ----------------------------------------------------------------------
# DISPATCH
# ----------------------------------------------------------------------
def run_option(op):
    if op == "1":
        perform_clean()
        normalize_python()
        perform_audit()
        compute_stats()
        update_baseline()
        apply_fixes()
        generate_governance()
        generate_tree()
    elif op == "2":
        perform_clean()
    elif op == "3":
        normalize_python()
    elif op == "4":
        perform_audit()
    elif op == "5":
        compute_stats()
    elif op == "6":
        update_baseline()
    elif op == "7":
        apply_fixes()
    elif op == "8":
        generate_governance()
    elif op == "9":
        generate_tree()
    elif op == "10":
        generate_tree_legacy()
    else:
        print("Opção inválida.")

# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
def main():
    print("\n==============================================")
    print("   MINDSCAN OPTIMIZER 2.3 — Leo Vinci")
    print("==============================================")

    if len(sys.argv) > 1:
        run_option(sys.argv[1].strip())
        return

    print("1 - ALL")
    print("2 - CLEAN")
    print("3 - NORMALIZE")
    print("4 - AUDIT")
    print("5 - STATS")
    print("6 - BASELINE")
    print("7 - FIXES")
    print("8 - GOVERNANCE")
    print("9 - FULLTREE")
    print("10 - TREE_LEGACY")
    print("0 - SAIR")
    op = input("Escolha: ").strip()
    if op == "0":
        return
    run_option(op)

if __name__ == "__main__":
    main()
