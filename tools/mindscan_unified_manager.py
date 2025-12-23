import os
import sys
import json
import shutil
import hashlib
import datetime
import sqlite3
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

# Tenta carregar o driver do Postgres para a nova funcionalidade
try:
    import psycopg2
    POSTGRES_SUPPORT = True
except ImportError:
    POSTGRES_SUPPORT = False

# ============================================================
# CONFIGURAÇÕES DE AMBIENTE (MINDSCAN CORE)
# ============================================================
SCRIPT_PATH = Path(__file__).resolve()
TOOLS_DIR = SCRIPT_PATH.parent
ROOT = TOOLS_DIR.parent  # D:\projetos-inovexa\mindscan
LOGS_DIR = ROOT / "logs"
AUDIT_DIR = LOGS_DIR / "audit"
STRUCTURE_LOGS = LOGS_DIR / "estrutura"
DB_LOCAL_PATH = ROOT / "mindscan_ms.db"

IGNORE_DIRS = {
    ".git", ".idea", ".vscode", "__pycache__", "venv", ".venv",
    "node_modules", "_optimizer_logs", "_optimizer_checkpoints",
    "logs", "backups_snapshots"
}

def ensure_paths():
    for p in [LOGS_DIR, AUDIT_DIR, STRUCTURE_LOGS]:
        p.mkdir(parents=True, exist_ok=True)

def log_event(msg: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

# ============================================================
# FUNCIONALIDADE 1: ÁRVORE ESTRUTURAL PREMIUM
# ============================================================

def op_generate_tree():
    """Gera visualização da estrutura com tamanhos e conexões."""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output = STRUCTURE_LOGS / f"tree_snapshot_{ts}.txt"
    log_event("Gerando árvore estrutural detalhada...")
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(f"MINDSCAN ARCHITECTURE SNAPSHOT - {ts}\nRaiz: {ROOT}\n{'='*70}\n\n")
        for curr, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            relative_curr = Path(curr).relative_to(ROOT)
            level = len(relative_curr.parts)
            indent = "    " * level
            
            f.write(f"{indent}├── [DIR] {os.path.basename(curr)}/\n")
            
            sub_indent = "    " * (level + 1)
            for i, filename in enumerate(files):
                fpath = Path(curr) / filename
                try:
                    size_kb = fpath.stat().st_size / 1024
                    size_display = f"({size_kb:.2f} KB)"
                except: size_display = "(Erro)"
                
                connector = "└── " if i == len(files) - 1 else "├── "
                f.write(f"{sub_indent}{connector}{filename} {size_display}\n")
                
    log_event(f"Árvore gerada com sucesso: {output}")

# ============================================================
# FUNCIONALIDADE 13: TESTE DE CONEXÃO POSTGRESQL
# ============================================================

def op_test_postgres():
    """Valida a conexão com o banco de produção (pgAdmin)."""
    print("\n[!] TESTANDO ACESSO AO POSTGRESQL (PRODUÇÃO)...")
    if not POSTGRES_SUPPORT:
        log_event("ERRO: Biblioteca 'psycopg2' não encontrada. Use: pip install psycopg2")
        return

    # Configuração baseada na sua infraestrutura atual
    config = {
        "dbname": "mindscan_db",
        "user": "postgres",
        "password": "sua_senha_aqui", # O Orion recomenda conferir o arquivo .env
        "host": "localhost",
        "port": "5432"
    }

    try:
        conn = psycopg2.connect(**config)
        log_event("CONEXÃO ESTABELECIDA COM SUCESSO AO POSTGRES!")
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = [t[0] for t in cur.fetchall()]
        print(f"    Tabelas detectadas no pgAdmin: {', '.join(tables)}")
        conn.close()
    except Exception as e:
        log_event(f"FALHA NA CONEXÃO: {e}")

# ============================================================
# LIMPEZA, SNAPSHOT E SAÚDE DO BANCO LOCAL
# ============================================================

def op_deep_cleanup():
    print("\n[!] INICIANDO LIMPEZA PROFUNDA...")
    confirm = input("Deletar arquivos lixo e corrigir redundância de backups? (s/n): ")
    if confirm.lower() != 's': return
    
    files_removed = 0
    bad_backup = ROOT / "_logging_fix_backup"
    if bad_backup.exists():
        shutil.rmtree(bad_backup)
        log_event("Pasta recursiva removida.")

    for fpath in ROOT.rglob('*'):
        if fpath.is_file():
            is_trash = (fpath.suffix in ['.tmp', '.bak', '.old', '.log'] or fpath.stat().st_size == 0)
            if is_trash and "logs" not in str(fpath) and fpath.name != "mindscan_ms.db":
                try:
                    fpath.unlink()
                    files_removed += 1
                except: continue
    log_event(f"Limpeza concluída. {files_removed} arquivos limpos.")

def op_db_local():
    if not DB_LOCAL_PATH.exists():
        log_event("Banco local mindscan_ms.db não encontrado.")
        return
    conn = sqlite3.connect(DB_LOCAL_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(f"    Tabelas no SQLite Local: {[t[0] for t in cur.fetchall()]}")
    conn.close()

def op_snapshot():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name = ROOT / f"MINDSCAN_SNAPSHOT_{ts}.zip"
    with ZipFile(name, 'w', ZIP_DEFLATED) as z:
        for f in ROOT.rglob('*'):
            if any(i in f.parts for i in IGNORE_DIRS) or f.suffix == '.zip': continue
            if f.is_file(): z.write(f, f.relative_to(ROOT))
    log_event(f"Backup ZIP criado: {name.name}")

# ============================================================
# MENU PRINCIPAL
# ============================================================

def main():
    ensure_paths()
    while True:
        print(f"\n{'='*65}")
        print(f"      MINDSCAN COMMAND CENTER v5.4 - ORION (POSTGRES READY)")
        print(f"{'='*65}")
        print(" [1]  Gerar Árvore Completa (Tamanho + Conexões)")
        print(" [4]  Auditoria de Integridade (JSON)")
        print(" [11] Limpeza Profunda (Exterminar Lixo e Loops de Pasta)")
        print(" [12] Verificar Banco LOCAL (SQLite)")
        print(" [13] TESTAR CONEXÃO POSTGRES (Produção pgAdmin)")
        print(" [14] Criar Snapshot Total (Backup em ZIP)")
        print(" [0]  Sair")
        
        choice = input("\nSelecione o comando > ").strip()
        if choice == "1": op_generate_tree()
        elif choice == "4": op_audit() # Chamando a lógica de auditoria interna
        elif choice == "11": op_deep_cleanup()
        elif choice == "12": op_db_local()
        elif choice == "13": op_test_postgres()
        elif choice == "14": op_snapshot()
        elif choice == "0": break

if __name__ == "__main__":
    main()