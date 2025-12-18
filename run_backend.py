"""
MindScan — Backend Runner (path-agnostic)

Objetivo:
- Subir o backend SEM depender do diretório atual (cwd)
- Resolver automaticamente o caminho correto do ASGI app:
    1) backend.app:app
    2) mindscan.backend.app:app
    3) backend.main:app
    4) mindscan.backend.main:app
- Permitir start via:  python run_backend.py
"""

from __future__ import annotations

import argparse
import importlib
import os
import sys
from pathlib import Path
from typing import Any, Optional


def _ensure_sys_path() -> None:
    """
    Garante que:
    - A raiz do repo (onde este arquivo mora) esteja no sys.path
    - O pacote 'mindscan' (se existir como diretório) também seja importável
    """
    repo_root = Path(__file__).resolve().parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    pkg_dir = repo_root / "mindscan"
    if pkg_dir.exists() and pkg_dir.is_dir():
        # Não insere pkg_dir direto (evita shadowing), mas garante visibilidade do pacote.
        # Em geral, repo_root já basta; isso aqui é só um “airbag”.
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))


def _try_import_app(module_path: str, attr: str = "app") -> Optional[Any]:
    """
    Tenta importar module_path e retornar o atributo `attr`.
    Retorna None se falhar.
    """
    try:
        mod = importlib.import_module(module_path)
        return getattr(mod, attr)
    except Exception:
        return None


def resolve_asgi_app() -> tuple[str, Any]:
    """
    Retorna (import_string, app_object).
    """
    candidates = [
        ("backend.app", "app"),
        ("mindscan.backend.app", "app"),
        ("backend.main", "app"),
        ("mindscan.backend.main", "app"),
    ]

    for mod_path, attr in candidates:
        app_obj = _try_import_app(mod_path, attr)
        if app_obj is not None:
            return f"{mod_path}:{attr}", app_obj

    raise RuntimeError(
        "Não foi possível resolver o ASGI app. Tentativas: "
        + ", ".join([f"{m}:{a}" for m, a in candidates])
    )


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MindScan — Backend Runner")
    p.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    p.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")))
    p.add_argument("--reload", action="store_true", default=False)
    p.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "info"))
    return p


def main() -> int:
    _ensure_sys_path()

    args = build_arg_parser().parse_args()

    # Importa uvicorn somente quando necessário (reduz falhas de import em contextos não-server)
    try:
        import uvicorn  # type: ignore
    except Exception as e:
        raise RuntimeError(f"uvicorn não disponível: {e!r}") from e

    import_string, _app_obj = resolve_asgi_app()

    # Executa via string para manter reload compatível
    uvicorn.run(
        import_string,
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
