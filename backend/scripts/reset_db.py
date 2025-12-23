import sys
import os
from datetime import datetime
from sqlalchemy import text

# Ajuste para encontrar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import SessionLocal, engine
from models.models import Usuario, Base

def reset_total():
    print("--- ⚠️ Iniciando Reset Total com CASCADE ---")
    connection = engine.connect()
    trans = connection.begin()
    try:
        # Resolve o erro do print: dropa com CASCADE para remover dependências
        connection.execute(text("DROP TABLE IF EXISTS usuarios CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS diagnosticos CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS respostas_brutas CASCADE;"))
        trans.commit()
        print("✅ Tabelas antigas removidas.")
        
        # Cria as tabelas novas conforme o seu models.py
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        # Insere o seu registo para a demonstração
        novo = Usuario(nome="Adonis Inovexa", email="diretoria@inovexa.com", data=datetime.now())
        db.add(novo)
        db.commit()
        db.close()
        print("🚀 SUCESSO: Banco limpo e pronto para o Nilo!")
    except Exception as e:
        trans.rollback()
        print(f"❌ Erro crítico: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    reset_total()