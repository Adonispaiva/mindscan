import os
import shutil
import json
from datetime import datetime

ROOT_PATH = r"D:\projetos-inovexa\mindscan"
LOG_FILE = os.path.join(ROOT_PATH, "logs", f"audit_clean_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
BACKUP_DIR = os.path.join(ROOT_PATH, "backup", f"audit_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

# Palavras-chave de arquivos a eliminar
TRASH_PATTERNS = ['duplicado', 'antigo', 'cópia', 'backup', 'tmp', 'temp', '.old', '.bak']

def list_files_recursive(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            yield os.path.join(root, file)

def is_trash(file_name):
    name_lower = file_name.lower()
    return any(keyword in name_lower for keyword in TRASH_PATTERNS)

def clean_project():
    log_data = {'start_time': str(datetime.now()), 'removed': [], 'backed_up': [], 'normalized': []}
    os.makedirs(BACKUP_DIR, exist_ok=True)

    for file_path in list_files_recursive(ROOT_PATH):
        file_name = os.path.basename(file_path)

        # Ignorar logs e backups
        if 'logs' in file_path or 'backup' in file_path:
            continue

        # Remover lixo duplicado
        if is_trash(file_name):
            backup_path = os.path.join(BACKUP_DIR, file_name)
            shutil.move(file_path, backup_path)
            log_data['removed'].append(file_path)
            continue

        # Normalizar nomes com (1), (2), etc.
        if '(' in file_name and ')' in file_name:
            new_name = file_name.split('(')[0].strip() + os.path.splitext(file_name)[1]
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            if not os.path.exists(new_path):
                os.rename(file_path, new_path)
                log_data['normalized'].append({'old': file_path, 'new': new_path})
            else:
                shutil.move(file_path, os.path.join(BACKUP_DIR, file_name))
                log_data['backed_up'].append(file_path)

    log_data['end_time'] = str(datetime.now())

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

    print(f"Limpeza e auditoria profunda concluídas. Relatório salvo em: {LOG_FILE}")

if __name__ == "__main__":
    print("Iniciando limpeza profunda do MindScan...")
    clean_project()
    print("Processo completo. Verifique os logs para detalhes.")
