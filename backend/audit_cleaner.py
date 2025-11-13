import os
import shutil
import json
from datetime import datetime

# Caminho raiz do projeto MindScan
ROOT_PATH = r"D:\projetos-inovexa\mindscan"
BACKUP_PATH = os.path.join(ROOT_PATH, 'backup', f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
LOG_FILE = os.path.join(ROOT_PATH, 'logs', f'structure_manager_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json')

# Estrutura padrão esperada
EXPECTED_STRUCTURE = {
    'backend': ['main.py', 'routers', 'models', 'services', 'database'],
    'frontend': ['src', 'public', 'package.json'],
    'MI': ['mi_core.py', 'algorithms', 'reports'],
    'docs': [],
    'scripts': [],
    'tests': [],
    'infra': [],
    'logs': []
}

# Extensões válidas por categoria
CATEGORY_EXTENSIONS = {
    'backend': ['.py'],
    'frontend': ['.tsx', '.js', '.jsx', '.ts'],
    'docs': ['.md', '.pdf', '.docx'],
    'MI': ['.py', '.md'],
    'scripts': ['.py', '.bat', '.ps1'],
    'assets': ['.png', '.jpg', '.jpeg', '.svg']
}

def ensure_structure():
    """Cria as pastas padrão se não existirem."""
    for folder in EXPECTED_STRUCTURE.keys():
        path = os.path.join(ROOT_PATH, folder)
        os.makedirs(path, exist_ok=True)

def classify_file(file_name):
    """Classifica o arquivo conforme extensão e categoria."""
    ext = os.path.splitext(file_name)[1].lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if ext in extensions:
            return category
    return 'unknown'

def move_file(src, dest_folder):
    """Move arquivo para o diretório correspondente, mantendo backups."""
    os.makedirs(dest_folder, exist_ok=True)
    dest_file = os.path.join(dest_folder, os.path.basename(src))
    if os.path.exists(dest_file):
        os.makedirs(BACKUP_PATH, exist_ok=True)
        shutil.move(dest_file, os.path.join(BACKUP_PATH, os.path.basename(dest_file)))
    shutil.move(src, dest_folder)

def generate_placeholder(file_path):
    """Cria arquivo placeholder com metadados de geração."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# Placeholder gerado automaticamente pelo MindScan Structure Manager\n# Data: {datetime.now()}\n")

def verify_and_rebuild_structure():
    """Garante que toda a estrutura obrigatória está presente e cria placeholders faltantes."""
    for folder, contents in EXPECTED_STRUCTURE.items():
        folder_path = os.path.join(ROOT_PATH, folder)
        os.makedirs(folder_path, exist_ok=True)
        for item in contents:
            item_path = os.path.join(folder_path, item)
            if not os.path.exists(item_path):
                if '.' in item:
                    generate_placeholder(item_path)
                else:
                    os.makedirs(item_path, exist_ok=True)

def audit_and_clean():
    """Audita e limpa a estrutura principal do MindScan."""
    log_data = {'start_time': str(datetime.now()), 'actions': []}
    ensure_structure()

    for item in os.listdir(ROOT_PATH):
        item_path = os.path.join(ROOT_PATH, item)

        # Ignorar pastas esperadas e ocultas
        if os.path.isdir(item_path) and item in EXPECTED_STRUCTURE.keys():
            continue

        if os.path.isdir(item_path) and item.startswith('.'):
            continue

        if os.path.isdir(item_path):
            shutil.move(item_path, BACKUP_PATH)
            log_data['actions'].append({'type': 'folder_backup', 'item': item})
            continue

        if os.path.isfile(item_path):
            category = classify_file(item)
            if category != 'unknown':
                dest_folder = os.path.join(ROOT_PATH, category)
                move_file(item_path, dest_folder)
                log_data['actions'].append({'type': 'move', 'file': item, 'destination': dest_folder})
            else:
                os.makedirs(BACKUP_PATH, exist_ok=True)
                shutil.move(item_path, os.path.join(BACKUP_PATH, item))
                log_data['actions'].append({'type': 'backup_unknown', 'file': item})

    verify_and_rebuild_structure()
    log_data['end_time'] = str(datetime.now())

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'w', encoding='utf-8') as logf:
        json.dump(log_data, logf, indent=4, ensure_ascii=False)

    print(f"Auditoria concluída. Log salvo em: {LOG_FILE}")

if __name__ == "__main__":
    print("Iniciando auditoria e limpeza do projeto MindScan...")
    audit_and_clean()
    print("Processo finalizado com sucesso.")
