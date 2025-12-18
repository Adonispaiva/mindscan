"""
MindScan Backend — Canonical ASGI entrypoint (sem duplicação de rotas)

Objetivos:
- Exportar `app: FastAPI` estável para `uvicorn backend.app:app`
- Garantir /health e /healthz SEM depender de routers externos
- Incluir APENAS o api_router (/api) quando disponível (evita rotas duplicadas)
- Fallback: se api_router não existir, inclui routers avulsos best-effort
- ✅ Incluir WebApp (/app) via import best-effort (sem quebrar boot)
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request


log = logging.getLogger("mindscan.app")


def _safe_import(module_path: str, attr: str) -> Optional[Any]:
    """
    Importa module_path e retorna getattr(attr) se existir.
    Falhas não bloqueiam boot.
    """
    try:
        module = __import__(module_path, fromlist=[attr])
        return getattr(module, attr, None)
    except Exception as e:
        logging.getLogger("mindscan.import").warning(
            "Import falhou: %s.%s | %s", module_path, attr, repr(e)
        )
        return None


def _include_router_best_effort(app: FastAPI, router: Any, name: str, prefix: str = "") -> None:
    """
    Inclui router se existir; falha não bloqueia boot.
    """
    if router is None:
        logging.getLogger("mindscan.router").info("Router ausente (skip): %s", name)
        return
    try:
        app.include_router(router, prefix=prefix)
        logging.getLogger("mindscan.router").info("Router incluído: %s", name)
    except Exception as e:
        logging.getLogger("mindscan.router").warning("Falha ao incluir router %s: %s", name, repr(e))


def _build_health_router():
    from fastapi import APIRouter

    r = APIRouter(tags=["Health"])

    @r.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @r.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok"}

    return r


def create_app() -> FastAPI:
    app = FastAPI(title="MindScan", version="1.0.0")

    # Handler de erro padrão (não deixar 500 “mudo”)
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception):
        logging.getLogger("mindscan.error").exception("Unhandled exception: %s", repr(exc))
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "message": "Unhandled server exception",
                "detail": str(exc),
            },
        )

    # Health canônico (sempre)
    app.include_router(_build_health_router())

    # Preferência: api_router único (evita duplicação de rotas)
    api_router = _safe_import("backend.routers.api_router", "api_router") or _safe_import(
        "backend.routers.api_router", "router"
    )
    if api_router is not None:
        _include_router_best_effort(app, api_router, "backend.routers.api_router", prefix="")
    else:
        # Fallback legacy: inclui routers avulsos (best-effort)
        _include_router_best_effort(app, _safe_import("backend.routers.diagnostic_router", "router"), "diagnostic", "")
        _include_router_best_effort(app, _safe_import("backend.routers.pdf_router", "router"), "pdf", "")

    # ✅ WebApp: inclui /app (tentando múltiplos caminhos para cobrir variações do projeto)
    # Contrato aceito:
    # - módulo expõe `router` (APIRouter)
    # - OU módulo expõe `get_router()` retornando APIRouter
    web_router = None

    get_router = _safe_import("web.router", "get_router")
    if callable(get_router):
        try:
            web_router = get_router()
        except Exception as e:
            logging.getLogger("mindscan.router").warning("Falha em web.router.get_router(): %s", repr(e))

    if web_router is None:
        web_router = _safe_import("web.web_app", "router")

    # fallback para variações "mindscan.web.*" (se existir no seu layout)
    if web_router is None:
        get_router2 = _safe_import("mindscan.web.router", "get_router")
        if callable(get_router2):
            try:
                web_router = get_router2()
            except Exception as e:
                logging.getLogger("mindscan.router").warning("Falha em mindscan.web.router.get_router(): %s", repr(e))
    if web_router is None:
        web_router = _safe_import("mindscan.web.web_app", "router")

    _include_router_best_effort(app, web_router, "webapp", prefix="")

    @app.on_event("startup")
    async def on_startup() -> None:
        log.info("MindScan backend booting...")
        init_db = _safe_import("backend.database", "init_db")
        if callable(init_db):
            try:
                maybe = init_db()
                if hasattr(maybe, "__await__"):
                    await maybe
                log.info("DB init: ok")
            except Exception as e:
                log.warning("DB init falhou (não bloqueante): %s", repr(e))
        else:
            log.info("DB init: não encontrado (skip)")

    return app


app = create_app()

__all__ = ["app", "create_app"]
