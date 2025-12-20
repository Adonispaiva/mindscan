import os
import sys
import logging
import subprocess

# Configuração de Log para o Diagnóstico
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("MindScan.Diagnostic")

def run_diagnostic():
    print("\n" + "="*60)
    print("🔍 DIAGNÓSTICO DE AMBIENTE ULTRA SUPERIOR - MINDSCAN")
    print("="*60)

    # 1. Verificação de Versão e Path
    print(f"\n[1] SISTEMA E CAMINHOS")
    print(f"Python Version: {sys.version}")
    print(f"Current Directory: {os.getcwd()}")
    project_root = r"D:\projetos-inovexa\mindscan"
    print(f"Project Root esperado: {project_root}")
    if os.path.exists(project_root):
        print("✅ Pasta raiz do projeto localizada.")
    else:
        print("❌ ERRO: Pasta raiz não encontrada no caminho D:\\")

    # 2. Teste de Dependências
    print(f"\n[2] DEPENDÊNCIAS (BIBLIOTECAS)")
    libs = ['pandas', 'sqlalchemy', 'psycopg2', 'reportlab', 'fastapi', 'uvicorn', 'dotenv']
    for lib in libs:
        try:
            __import__(lib.replace('-', '_'))
            print(f"✅ {lib}: Instalada")
        except ImportError:
            print(f"❌ {lib}: NÃO ENCONTRADA (Execute: pip install {lib})")

    # 3. Teste do Arquivo .env
    print(f"\n[3] CONFIGURAÇÕES (.env)")
    env_path = os.path.join(project_root, ".env")
    if os.path.exists(env_path):
        print(f"✅ Arquivo .env localizado em: {env_path}")
        from dotenv import load_dotenv
        load_dotenv(env_path)
        print(f"   DB_NAME: {os.getenv('DB_NAME')}")
        print(f"   DB_USER: {os.getenv('DB_USER')}")
    else:
        print(f"❌ ERRO: Arquivo .env não encontrado em {env_path}")

    # 4. Teste de Conexão com Banco de Dados
    print(f"\n[4] CONEXÃO POSTGRESQL")
    try:
        from sqlalchemy import create_engine, text
        db_user = os.getenv("DB_USER", "postgres")
        db_pass = os.getenv("DB_PASS", "sua_senha_aqui")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "mindscan")
        
        url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"✅ Conexão com o banco '{db_name}' estabelecida com sucesso!")
    except Exception as e:
        print(f"❌ ERRO DE CONEXÃO: {str(e)}")

    # 5. Verificação de Ativos Críticos
    print(f"\n[5] ATIVOS E ARQUIVOS")
    csv_path = os.path.join(project_root, "backend", "data", "relatorio_emilia.csv")
    if os.path.exists(csv_path):
        print(f"✅ CSV da Emília localizado: {csv_path}")
    else:
        print(f"❌ ERRO: CSV não encontrado em {csv_path}")

    report_dir = os.path.join(project_root, "generated_reports")
    if not os.path.exists(report_dir):
        try:
            os.makedirs(report_dir)
            print(f"✅ Pasta de relatórios criada: {report_dir}")
        except Exception as e:
            print(f"❌ ERRO ao criar pasta de relatórios: {e}")
    else:
        print(f"✅ Pasta de relatórios pronta: {report_dir}")

    print("\n" + "="*60)
    print("FIM DO DIAGNÓSTICO")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_diagnostic()