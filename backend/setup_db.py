import sys
import os
import logging

# 1. FORÇAR CAMINHOS ABSOLUTOS (A SOLUÇÃO REAL)
BASE_DIR = r"D:\projetos-inovexa\mindscan"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 2. IMPORTAÇÕES APÓS A INJEÇÃO DO CAMINHO
try:
    from backend.database import engine, Base
    from backend.models import Diagnostic
    print("✅ Conexão interna estabelecida.")
except Exception as e:
    print(f"❌ Erro de importação: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SetupDB")

def initialize_database():
    print("\n" + "="*50)
    print("🚀 MINDSCAN - INICIALIZAÇÃO DE BANCO")
    print("="*50)
    try:
        # Comando que cria as tabelas no PostgreSQL
        Base.metadata.create_all(bind=engine)
        print("\n✅ SUCESSO ABSOLUTO: Tabelas criadas no Postgres!")
    except Exception as e:
        print(f"❌ ERRO NO POSTGRES: {e}")
        print("Certifique-se que o banco 'mindscan' foi criado no pgAdmin.")

if __name__ == "__main__":
    initialize_database()