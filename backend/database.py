# Caminho: backend/database.py
# MindScan Backend — Núcleo de Banco de Dados
# Diretor Técnico: Leo Vinci (Inovexa Software)
#
# Versão Final — Integrado ao sistema oficial de settings (pysettings)
# Compatível com SQLAlchemy 2.0 e execução via módulo

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pysettings import get_settings

# ============================================================
# 1) SETTINGS OFICIAIS
# ============================================================

settings = get_settings()
DATABASE_URL = settings.DATABASE_URL

# ============================================================
# 2) BASE DO ORM
# ============================================================

Base = declarative_base()

# ============================================================
# 3) ENGINE (sincrono) — compatível com migrações
# ============================================================

engine = create_engine(
    DATABASE_URL.replace("+asyncpg", ""),  # fallback seguro para sync
    echo=False,
    future=True
)

# ============================================================
# 4) SESSION FACTORY
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ============================================================
# 5) DEPENDÊNCIA FASTAPI
# ============================================================

def get_db():
    """
    Dependência FastAPI que gera e encerra uma sessão SQLAlchemy
    de maneira segura.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
