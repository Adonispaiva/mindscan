import os
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MindScan.Database")

# Localiza o .env na raiz do projeto - Preservando sua lógica original
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mindscan_db")

URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# A Base deve ser definida aqui e exportada diretamente
Base = declarative_base()

try:
    # pool_pre_ping garante que conexões inativas do Postgres não quebrem o FastAPI
    engine = create_engine(URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info(f"✅ Database: Motor configurado para {DB_NAME} no PostgreSQL 18.1")
except Exception as e:
    logger.error(f"❌ Erro ao configurar banco de dados: {e}")
    sys.exit(1)