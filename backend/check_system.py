import socket
import sys
import os
from sqlalchemy import create_engine, text

# Adiciona o diretório ao path para testar os módulos reais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def test_db_direct():
    print("--- [1] Testando Conexão com PostgreSQL ---")
    try:
        # Importa as configurações do seu database.py
        from database import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Conexão com PostgreSQL: SUCESSO!")
            return True
    except Exception as e:
        print(f"❌ ERRO NO BANCO: {e}")
        print("\n💡 DICA: Verifique se o serviço do PostgreSQL está rodando e se a senha no .env está correta.")
        return False

def test_port_8000():
    print("\n--- [2] Testando Porta 8000 ---")
    if check_port(8000):
        print("⚠️ PORTA 8000 JÁ EM USO! Outro processo está usando esta porta.")
    else:
        print("✅ PORTA 8000 LIVRE: Pronta para o MindScan.")

if __name__ == "__main__":
    print("="*60)
    print("MINDSCAN - DIAGNÓSTICO DE CONECTIVIDADE")
    print("="*60)
    
    db_ok = test_db_direct()
    test_port_8000()
    
    print("\n" + "="*60)
    if db_ok:
        print("🚀 TUDO PRONTO! Agora execute: python main.py")
        print("E mantenha a janela do terminal aberta!")
    else:
        print("❌ RESOLVA O ERRO DO BANCO ANTES DE SUBIR A API.")
    print("="*60)