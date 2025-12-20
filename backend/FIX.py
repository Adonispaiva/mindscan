import sys
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# --- CONFIGURACAO DIRETA (SEM .ENV) ---
# Substitua SUA_SENHA_AQUI pela senha do seu pgAdmin
DB_URL = "postgresql://postgres:SUA_SENHA_AQUI@127.0.0.1:5432/mindscan_db"

Base = declarative_base()
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    email = Column(String(255), unique=True)

if __name__ == "__main__":
    print("Tentando conexao direta via IP (Ignorando Path)...")
    try:
        Base.metadata.create_all(bind=engine)
        print("MINDSCAN_OK: Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"Erro: {str(e)}")