#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import zipfile
from pathlib import Path
from typing import Iterable, Set, Tuple


DEFAULT_EXCLUDE_DIRS = {
    ".git",
    "venv",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".cache",
}

DEFAULT_EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".log",
    ".tmp",
    ".bak",
    ".swp",
    ".swo",
}

DEFAULT_EXCLUDE_FILES = {
    ".DS_Store",
    "Thumbs.db",
}


def should_exclude(path: Path, rel_parts_lower: Tuple[str, ...], exclude_dirs: Set[str], exclude_exts: Set[str], exclude_files: Set[str]) -> bool:
    name_lower = path.name.lower()

    # Excluir nomes de arquivo explícitos
    if name_lower in exclude_files:
        return True

    # Excluir por extensão
    if path.is_file():
        if path.suffix.lower() in exclude_exts:
            return True

    # Excluir por diretórios (qualquer segmento do caminho)
    for part in rel_parts_lower:
        if part in exclude_dirs:
            return True

    return False


def iter_files(src: Path, exclude_dirs: Set[str], exclude_exts: Set[str], exclude_files: Set[str]) -> Iterable[Tuple[Path, Path]]:
    """
    Yield (abs_path, rel_path) para arquivos elegíveis.
    """
    for p in src.rglob("*"):
        try:
            if not p.is_file():
                continue
        except OSError:
            # arquivo inacessível
            continue

        rel = p.relative_to(src)
        rel_parts_lower = tuple(part.lower() for part in rel.parts)

        if should_exclude(p, rel_parts_lower, exclude_dirs, exclude_exts, exclude_files):
            continue

        yield p, rel


def main():
    ap = argparse.ArgumentParser(
        description="Gera um ZIP limpo do projeto (exclui .git, venv, node_modules, caches e lixo comum)."
    )
    ap.add_argument("--src", required=True, help="Pasta do projeto (ex.: D:\\\\projetos\\\\mindscan ou ./mindscan)")
    ap.add_argument("--out", default="mindscan_clean.zip", help="Arquivo ZIP de saída (default: mindscan_clean.zip)")
    ap.add_argument("--include-root", action="store_true",
                    help="Inclui a pasta raiz dentro do ZIP (ex.: mindscan/... em vez de arquivos direto na raiz do ZIP).")
    ap.add_argument("--no-default-excludes", action="store_true",
                    help="Não aplica exclusões padrão (use junto com --exclude-dir/--exclude-ext/--exclude-file).")

    ap.add_argument("--exclude-dir", action="append", default=[], help="Diretório para excluir (pode repetir). Ex.: --exclude-dir .git")
    ap.add_argument("--exclude-ext", action="append", default=[], help="Extensão para excluir (pode repetir). Ex.: --exclude-ext .log")
    ap.add_argument("--exclude-file", action="append", default=[], help="Arquivo para excluir (pode repetir). Ex.: --exclude-file secrets.json")

    ap.add_argument("--write-filelist", action="store_true",
                    help="Gera também um arquivo .txt com a lista de arquivos incluídos no ZIP.")
    args = ap.parse_args()

    src = Path(args.src).expanduser().resolve()
    if not src.exists() or not src.is_dir():
        print(f"[ERRO] Pasta inválida: {src}", file=sys.stderr)
        sys.exit(2)

    out = Path(args.out).expanduser().resolve()
    if out.exists():
        out.unlink()

    if args.no_default_excludes:
        exclude_dirs = set(d.lower() for d in args.exclude_dir)
        exclude_exts = set(e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.exclude_ext)
        exclude_files = set(f.lower() for f in args.exclude_file)
    else:
        exclude_dirs = set(DEFAULT_EXCLUDE_DIRS) | set(d.lower() for d in args.exclude_dir)
        exclude_exts = set(DEFAULT_EXCLUDE_EXTS) | set(e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.exclude_ext)
        exclude_files = set(DEFAULT_EXCLUDE_FILES) | set(f.lower() for f in args.exclude_file)

    root_name = src.name
    included = 0
    skipped = 0
    filelist_lines = []

    compression = zipfile.ZIP_DEFLATED

    with zipfile.ZipFile(out, "w", compression=compression, compresslevel=9) as z:
        for abs_path, rel_path in iter_files(src, exclude_dirs, exclude_exts, exclude_files):
            arcname = str(rel_path).replace("\\", "/")
            if args.include_root:
                arcname = f"{root_name}/{arcname}"

            try:
                z.write(abs_path, arcname)
                included += 1
                if args.write_filelist:
                    filelist_lines.append(arcname)
            except OSError:
                skipped += 1

    if args.write_filelist:
        filelist_path = out.with_suffix(out.suffix + ".filelist.txt")
        filelist_path.write_text("\n".join(filelist_lines) + ("\n" if filelist_lines else ""), encoding="utf-8")
        print(f"[OK] Filelist: {filelist_path}")

    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"[OK] ZIP gerado: {out}")
    print(f"[OK] Incluídos: {included} | Pulados (erro de leitura): {skipped}")
    print(f"[OK] Tamanho: {size_mb:.2f} MB")
    print("[INFO] Exclusões ativas:")
    print(f"  - dirs: {sorted(exclude_dirs)}")
    print(f"  - exts: {sorted(exclude_exts)}")
    print(f"  - files: {sorted(exclude_files)}")


if __name__ == "__main__":
    main()
