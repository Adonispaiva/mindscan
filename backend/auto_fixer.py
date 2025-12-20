import os
import sys
import subprocess
import shutil

def log_status(msg, success=True):
    symbol = "✅" if success else "❌"
    print(f"{symbol} {msg}")

def run_step(name, command):
    print(f"\n--- [EXECUTANDO: {name}] ---")
    try:
        # Executa o comando e captura a saída para evitar poluição mas garantir feedback
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        log_status(name)
        return True
    except subprocess.CalledProcessError as e:
        log_status(f"FALHA EM {name}: {e.stderr}", False)
        return False

def fix_environment():
    print("="*60)
    print("🚀 INOVEZA SOFTWARE - REPARADOR AUTOMÁTICO MINDSCAN")
    print("="*60)

    # 1. Limpeza de Cache (Anti-Regressão)
    print("\n[1] Limpando resíduos de execução anterior...")
    backend_dir = r"D:\projetos-inovexa\mindscan\backend"
    pycache = os.path.join(backend_dir, "__pycache__")
    if os.path.exists(pycache):
        shutil.rmtree(pycache)
        log_status("Cache __pycache__ removido.")

    # 2. Instalação de Dependências Críticas
    print("\n[2] Validando e instalando bibliotecas necessárias...")
    dependencies = [
        "pandas", 
        "sqlalchemy", 
        "psycopg2-binary", 
        "reportlab", 
        "fastapi", 
        "uvicorn", 
        "python-dotenv"
    ]
    
    for lib in dependencies:
        run_step(f"Instalando {lib}", f"{sys.executable} -m pip install {lib}")

    # 3. Verificação de Arquivos Nucleares
    print("\n[3] Verificando integridade de arquivos...")
    required_files = ["database.py", "FORCA_BRUTA_SETUP.py", "ingest_emilia.py", "main.py"]
    for f in required_files:
        path = os.path.join(backend_dir, f)
        if os.path.exists(path):
            log_status(f"Arquivo localizado: {f}")
        else:
            log_status(f"Arquivo AUSENTE: {f}", False)

    # 4. Validação de Conectividade Base
    print("\n[4] Testando inicialização do motor de dados...")
    try:
        # Adiciona o diretório ao path para simular execução real
        if backend_dir not in sys.path:
            sys.path.append(backend_dir)
            
        import database
        log_status("Importação de 'database.py' bem-sucedida.")
    except Exception as e:
        log_status(f"Erro na importação do banco: {str(e)}", False)
        print("💡 DICA: Verifique se a senha no .env está correta.")

    print("\n" + "="*60)
    print("🏁 PROCEDIMENTO FINALIZADO")
    print("Tente rodar novamente: python main.py")
    print("="*60)

if __name__ == "__main__":
    fix_environment()