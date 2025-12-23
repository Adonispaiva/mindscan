import sys
import os
from datetime import datetime

# Ajuste de caminho para o Windows encontrar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import SessionLocal, engine
from models.models import Usuario, Base

def sincronizar_sistema():
    print("--- 🗑️ Resetando tabela para adicionar a coluna 'data' ---")
    # Este comando resolve o erro 'UndefinedColumn' do seu PowerShell
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Inserindo o seu registo de teste
        novo = Usuario(
            nome="Adonis Inovexa", 
            email="diretoria@inovexa.com", 
            data=datetime.now()
        )
        db.add(novo)
        db.commit()
        print("✅ SUCESSO: Tabela 'usuarios' recriada com a coluna 'data'!")
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    sincronizar_sistema()