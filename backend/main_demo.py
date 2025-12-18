"""
MindScan Backend — Demo entrypoint (compatível e não-concorrente)

Objetivos:
- Manter um "modo demo" sem criar um segundo boot divergente do sistema
- Evitar concorrência de mains: este arquivo DELEGA para o entrypoint canônico (backend.main / backend.app)
- Preservar compatibilidade: exporta `app`, `create_app`, `run`, `main`
- Acrescentar utilidades de demo apenas se existirem módulos auxiliares no projeto
  (best-effort: backend.utils.demo_payload, backend.start_demo, backend.scripts.run_demo)

Uso:
- uvicorn backend.main_demo:app
- python -m backend.main_demo
- python backend/main_demo.py
"""

from __future__ import annotations

import argparse
import importlib
import os
import sys
from typing import Any, Optional


def _safe_import(module_path: str, attr: Optional[str] = None) -> Any:
    """
    Import defensivo:
    - Se attr for None, retorna o módulo; se existir, retorna getattr(módulo, attr).
    - Em falha, retorna None.
    """
    try:
        mod = importlib.import_module(module_path)
        if attr is None:
            return mod
        return getattr(mod, attr, None)
    except Exception:
        return None


def _ensure_sys_path() -> None:
    """
    Airbag para execução como script.
    Não interfere quando executado como módulo.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(here)
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


def create_app() -> Any:
    """
    Fonte única do ASGI em modo demo:
    - prioridade: backend.main.create_app (já delega para backend.app.create_app)
    - fallback: backend.app.create_app
    - último recurso: FastAPI minimal com /health
    """
    fn = _safe_import("backend.main", "create_app")
    if callable(fn):
        app_obj = fn()
    else:
        fn2 = _safe_import("backend.app", "create_app")
        if callable(fn2):
            app_obj = fn2()
        else:
            from fastapi import FastAPI

            app_obj = FastAPI(title="MindScan Backend (demo-fallback)", version="0.0.0")

            @app_obj.get("/health")
            def health() -> dict[str, str]:
                return {"status": "ok", "service": "mindscan-backend", "mode": "demo-fallback"}

    # Enriquecimentos de demo (NÃO bloqueantes)
    try:
        from fastapi import APIRouter

        demo_router = APIRouter(prefix="/demo", tags=["demo"])

        # Expor payload de exemplo se existir
        payload_fn = _safe_import("backend.utils.demo_payload", "get_demo_payload") or _safe_import(
            "backend.utils.demo_payload", "build_demo_payload"
        )

        @demo_router.get("/payload")
        def demo_payload() -> dict[str, Any]:
            if callable(payload_fn):
                result = payload_fn()
                # normaliza para dict
                return result if isinstance(result, dict) else {"payload": result}
            return {"payload": None, "hint": "backend.utils.demo_payload não encontrado"}

        # Hook opcional para preparar demo (seed, mocks, etc.)
        demo_boot = _safe_import("backend.start_demo", "bootstrap_demo") or _safe_import(
            "backend.scripts.run_demo", "bootstrap_demo"
        )
        demo_run = _safe_import("backend.start_demo", "run") or _safe_import(
            "backend.scripts.run_demo", "run"
        )

        # Inclui router demo
        app_obj.include_router(demo_router)

        # Startup best-effort
        @app_obj.on_event("startup")
        async def _on_startup_demo() -> None:
            try:
                if callable(demo_boot):
                    maybe = demo_boot()
                    if hasattr(maybe, "__await__"):
                        await maybe
                # Algumas bases antigas usam run() para preparar recursos;
                # rodamos em best-effort e não bloqueamos boot.
                if callable(demo_run):
                    maybe2 = demo_run()
                    if hasattr(maybe2, "__await__"):
                        await maybe2
            except Exception:
                # Sem logging rígido aqui para evitar dependência;
                # backend.app já configura logging quando disponível.
                return

    except Exception:
        # Se FastAPI/routers não estiverem disponíveis por qualquer razão, não derruba o app.
        pass

    return app_obj


# Export ASGI
app = create_app()


def _resolve_uvicorn_import_string() -> str:
    """
    Para reload funcionar, uvicorn precisa de string "module:attr".
    Tentamos módulos mais prováveis.
    """
    candidates = [
        ("backend.main_demo", "app"),
        ("mindscan.backend.main_demo", "app"),
    ]
    for mod, attr in candidates:
        try:
            importlib.import_module(mod)
            return f"{mod}:{attr}"
        except Exception:
            continue
    return ""


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MindScan Backend — Demo Runner")
    p.add_argument("--host", default=os.getenv("HOST", os.getenv("MINDSCAN_HOST", "127.0.0.1")))
    p.add_argument("--port", type=int, default=int(os.getenv("PORT", os.getenv("MINDSCAN_PORT", "8000"))))
    p.add_argument("--reload", action="store_true", default=os.getenv("RELOAD", "0") == "1")
    p.add_argument("--log-level", default=os.getenv("LOG_LEVEL", os.getenv("MINDSCAN_LOG_LEVEL", "info")))
    return p


def run(host: str, port: int, reload: bool, log_level: str) -> None:
    """
    Runner programático em modo demo.
    """
    try:
        import uvicorn  # type: ignore
    except Exception as e:
        raise RuntimeError(f"uvicorn não disponível: {e!r}") from e

    import_string = _resolve_uvicorn_import_string()

    if import_string:
        uvicorn.run(import_string, host=host, port=port, reload=reload, log_level=log_level)
        return

    uvicorn.run(app, host=host, port=port, reload=False, log_level=log_level)


def main(argv: Optional[list[str]] = None) -> int:
    _ensure_sys_path()
    args = build_arg_parser().parse_args(argv)
    run(host=args.host, port=args.port, reload=args.reload, log_level=args.log_level)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
