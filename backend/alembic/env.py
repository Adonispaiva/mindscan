import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# =====================================================
# FIX DEFINITIVO DE PATH — ÁRVORE REAL DO PROJETO
# =====================================================
# Estrutura validada:
# mindscan/
#   backend/
#     alembic/
#     db/
#     config.py
#     models.py
#     ...

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
# =====================================================

# IMPORTS REAIS (SEM PREFIXO backend.)
from db.base import Base
from config import settings

# Alembic Config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata central do projeto
target_metadata = Base.metadata


def get_database_url() -> str:
    """
    Fonte única da URL do banco.
    Centralizada em config/settings.
    """
    return settings.DATABASE_URL


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    """
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
