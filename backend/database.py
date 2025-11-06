from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# -------------------------------------------------------------------------
# Configuração do banco de dados MindScan
# -------------------------------------------------------------------------

# URL de conexão assíncrona (pode ser sobrescrita via variável de ambiente)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./mindscan.db")

# Engine assíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # definir True apenas em debug
    future=True
)

# Sessão assíncrona
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base declarativa para os modelos
Base = declarative_base()

# -------------------------------------------------------------------------
# Função auxiliar para inicialização do banco (opcional)
# -------------------------------------------------------------------------
async def init_db():
    """Cria as tabelas no banco de dados de forma assíncrona."""
    import models.user  # garante registro das entidades
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
