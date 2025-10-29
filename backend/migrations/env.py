import asyncio
import sys
import os
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context

# Ajuste de path para importar models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Base  # noqa
from config import DATABASE_URL

# Configuração do Alembic
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Função assíncrona de migração
async def run_async_migrations():
    from sqlalchemy.ext.asyncio import create_async_engine

    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool
    )

    async with connectable.begin() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    asyncio.run(run_async_migrations())

run_migrations_online()
