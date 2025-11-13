"""
Módulo de banco de dados desacoplado do MindScan.

Fornece:
- engine        -> instância do SQLAlchemy Engine
- SessionLocal  -> fábrica de sessões
- Base          -> classe base declarativa
- init_db()     -> criação das tabelas
- get_db()      -> dependência padrão para FastAPI
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import DATABASE_URL
from backend.models.base import Base


# ---------------------------------------------------------------------
# Engine e Session
# ---------------------------------------------------------------------

# Para SQLite precisamos do connect_args específico.
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------
# Inicialização do banco (criação de tabelas)
# ---------------------------------------------------------------------


def init_db() -> None:
    """
    Inicializa o banco criando as tabelas necessárias.

    Importamos os modelos aqui dentro para garantir que o metadata
    conheça todas as entidades antes de criar as tabelas.
    """
    # Importar todos os modelos que possuem tabelas
    # (adicione novos aqui conforme forem surgindo)
    import backend.models.quiz  # noqa: F401

    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------
# Dependência padrão para FastAPI
# ---------------------------------------------------------------------


def get_db() -> Generator[Session, None, None]:
    """
    Dependência de sessão de banco para usar nas rotas FastAPI.

    Exemplo de uso na rota:
        def list_quizzes(db: Session = Depends(get_db)):
            ...
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
