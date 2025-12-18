# Arquivo: backend/database.py
# MindScan Backend — Database Layer (SQLAlchemy)
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão: 2.0.1 (hotfix)

from __future__ import annotations

import os
import json
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# =============================================================================
# Config
# =============================================================================

DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("SQLALCHEMY_DATABASE_URL")
    or os.getenv("MINDSCAN_DATABASE_URL")
    # Default dev: SQLite local (não exige infra)
    or "sqlite:///./mindscan.db"
)

_is_sqlite = DATABASE_URL.startswith("sqlite:")

_engine_kwargs = {
    "pool_pre_ping": True,
    "future": True,
}
if _is_sqlite:
    # SQLite: FastAPI multi-thread safe
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


# =============================================================================
# Session helpers
# =============================================================================

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa o schema (create_all) em ambientes sem Alembic.
    Em produção, preferir migrações (alembic), mas isso garante smoke-test.
    """
    # Importa models para registrar metadata
    try:
        import backend.models  # noqa: F401
    except Exception:
        # Não bloqueia boot — app.py faz startup best-effort
        return
    Base.metadata.create_all(bind=engine)


# =============================================================================
# Legacy (compatibilidade) — ExportService veio parar aqui por erro de nomeação.
# Mantido para não perder funcionalidade e para evitar regressão.
# =============================================================================

class ExportService:
    """
    (LEGACY) Exporta dados em CSV. Mantido por compatibilidade.
    Preferir backend.services.export_service.ExportService.
    """

    def export(self, test_id: int) -> str:
        from pathlib import Path
        from backend.models import Result  # import local evita ciclo
        from sqlalchemy import desc

        exports_dir = Path("exports")
        exports_dir.mkdir(parents=True, exist_ok=True)

        # tenta ler resultados reais do DB (último registro)
        db = SessionLocal()
        try:
            last = (
                db.query(Result)
                .filter(Result.test_id == test_id)
                .order_by(desc(Result.id))
                .first()
            )
            payload = {}
            if last and last.results:
                try:
                    payload = json.loads(last.results)
                except Exception:
                    payload = {"raw": last.results}
        finally:
            db.close()

        file_path = exports_dir / f"results_{test_id}.csv"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("dimension,score,descriptor\n")
            if isinstance(payload, list):
                for item in payload:
                    if isinstance(item, dict):
                        file.write(
                            f"{item.get('dimension','')},{item.get('score','')},{_csv_sanitize(item.get('descriptor',''))}\n"
                        )
            elif isinstance(payload, dict):
                for k, v in payload.items():
                    file.write(f"{k},,{_csv_sanitize(v)}\n")

        return str(file_path)


def _csv_sanitize(value) -> str:
    s = "" if value is None else str(value)
    s = s.replace("\n", " ").replace("\r", " ").replace(",", ";")
    return s
