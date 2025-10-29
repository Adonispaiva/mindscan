from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

from .config import DATABASE_URL, ALLOWED_ORIGINS
from routers import quiz, auth, admin, health, user, response

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy async
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

app = FastAPI(title="MindScan API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "MindScan API rodando com PostgreSQL + asyncpg."}

@app.get("/status")
async def status_check():
    return {"status": "ok", "db": DATABASE_URL.split('/')[-1]}

@app.on_event("startup")
async def startup_event():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Conexão com banco e estrutura validadas com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com banco de dados: {e}")

# Routers
app.include_router(quiz.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(health.router)
app.include_router(user.router)
app.include_router(response.router)
