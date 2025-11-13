from pathlib import Path
import os
import shutil

# Diretório raiz do MindScan
ROOT = Path(r"D:\projetos-inovexa\mindscan")

# Estrutura da nova hierarquia
STRUCTURE = {
    "scripts": ["push", "setup", "run"],
    "tools": [],
    "maintenance": ["logs", "reports"],
    "env": []
}

# Arquivos e seus novos destinos
FILE_MAP = {
    "push_clean_git.bat": "scripts/push/",
    "push_github_mindscan.bat": "scripts/push/",
    "push_mindscan.bat": "scripts/push/",
    "limpa-repo.ps1": "scripts/maintenance/",
    "verificar_auditoria_mindscan_v2.1.ps1": "tools/",
    "verificar_duplicidade_mindscan.py": "tools/",
    "remover_duplicado_automacao.py": "tools/",
    "diagnostico_mindscan_SAFE.py": "tools/",
    "setup_backend.bat": "scripts/setup/",
    "setup_frontend.bat": "scripts/setup/",
    "run-api.ps1": "scripts/run/",
    "run-web.ps1": "scripts/run/",
    "start_all.bat": "scripts/run/",
}

def create_structure():
    """Cria a estrutura de diretórios padrão Inovexa Factory."""
    for base, subfolders in STRUCTURE.items():
        base_path = ROOT / base
        base_path.mkdir(exist_ok=True)
        for sub in subfolders:
            (base_path / sub).mkdir(exist_ok=True)
    print("🧩 Estrutura de diretórios criada com sucesso.")

def move_files():
    """Move os arquivos para seus novos destinos."""
    for file_name, dest_rel in FILE_MAP.items():
        src = ROOT / file_name
        dest = ROOT / dest_rel / file_name
        if src.exists():
            shutil.move(str(src), str(dest))
            print(f"✅ Movido: {src.name} → {dest_rel}")
        else:
            print(f"⚠️  Arquivo não encontrado: {src.name}")

def update_gitignore():
    """Atualiza o .gitignore com novas regras."""
    gitignore_path = ROOT / ".gitignore"
    additions = [
        "\n# Logs e relatórios",
        "/maintenance/logs/",
        "/maintenance/reports/",
        "*.log"
    ]
    with open(gitignore_path, "a", encoding="utf-8") as f:
        f.write("\n".join(additions))
    print("🧠 .gitignore atualizado com exclusões de logs e relatórios.")

def main():
    print("🔧 MindScan Directory Mapper v1.0 — Inovexa Factory Layout")
    create_structure()
    move_files()
    update_gitignore()
    print("\n🏁 Reorganização concluída com sucesso.")

if __name__ == "__main__":
    main()
