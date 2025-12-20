# -*- coding: utf-8 -*-
import sys
import os

# BLINDAGEM DE ENCODING: Força o console a aceitar caracteres brasileiros ou ignorar erros
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, JSON, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

# Configuração direta para evitar erro de leitura no .env
# Como seu Postgres está no Drive D com porta 5432 e modo trust:
DATABASE_URL = "postgresql://postgres@127.0.0.1:5432/postgres"

Base = declarative_base()

# --- DEFINIÇÃO DO SCHEMA (RECONSTRUÍDO) ---

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    email = Column(String(255), unique=True)
    data_nascimento = Column(String(50))
    loja = Column(String(255))
    funcao = Column(String(255))
    criado_em = Column(DateTime, server_default=func.now())

class Resposta(Base):
    __tablename__ = "respostas"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    pergunta_id = Column(Integer)
    valor_resposta = Column(Integer)
    texto_original = Column(Text)

class Diagnostico(Base):
    __tablename__ = "diagnosticos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    json_data = Column(JSON)
    pdf_path = Column(String(512))
    criado_em = Column(DateTime, server_default=func.now())

# --- EXECUÇÃO DA FORÇA BRUTA ---

def executar_setup():
    print("--- INICIANDO SETUP MINDSCAN (MODO FORÇA BRUTA) ---")
    try:
        # 1. Conecta ao Postgres (Banco padrão)
        engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
        
        # 2. Tenta criar o banco de dados mindscan_db se não existir
        with engine.connect() as conn:
            print("Verificando existencia do banco 'mindscan_db'...")
            exists = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='mindscan_db'")).fetchone()
            if not exists:
                conn.execute(text("CREATE DATABASE mindscan_db"))
                print("Banco 'mindscan_db' criado com sucesso.")
            else:
                print("Banco 'mindscan_db' ja existe.")

        # 3. Conecta ao novo banco para criar as tabelas
        APP_DB_URL = "postgresql://postgres@127.0.0.1:5432/mindscan_db"
        app_engine = create_engine(APP_DB_URL)
        
        print("Criando tabelas (Usuarios, Respostas, Diagnosticos)...")
        Base.metadata.create_all(app_engine)
        
        print("\n[SUCESSO]: A Via Crucis do Banco de Dados terminou.")
        print("As tabelas foram criadas e o MindScan esta pronto para operar.")

    except Exception as e:
        print(f"\n[ERRO FATAL]: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    executar_setup()