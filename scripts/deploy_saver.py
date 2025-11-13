import os
import shutil
import json
from datetime import datetime

ROOT_PATH = r"D:\projetos-inovexa\mindscan"
DEPLOY_TARGETS = {
    "backend": r"D:\SynMind\deploy\MindScan\backend",
    "frontend": r"D:\SynMind\deploy\MindScan\frontend",
    "MI": r"D:\SynMind\deploy\MindScan\MI",
    "docs": r"D:\SynMind\deploy\MindScan\docs"
}
LOG_FILE = os.path.join(ROOT_PATH, "logs", f"deploy_saver_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def ensure_targets():
    """Cria diretórios de destino se não existirem."""
    for path in DEPLOY_TARGETS.values():
        os.makedirs(path, exist_ok=True)

def deploy_folder(source, destination):
    """Copia ou atualiza o conteúdo da pasta."""
    if not os.path.exists(source):
        return None
    for root, _, files in os.walk(source):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(root, source)
            dest_dir = os.path.join(destination, rel_path)
            os.makedirs(dest_dir, exist_ok=True)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dest_file)

def deploy_all():
    """Executa o deploy completo."""
    log_data = {"start_time": str(datetime.now()), "deployed": []}
    ensure_targets()

    for folder, dest in DEPLOY_TARGETS.items():
        source = os.path.join(ROOT_PATH, folder)
        if os.path.exists(source):
            deploy_folder(source, dest)
            log_data["deployed"].append({"from": source, "to": dest})

    log_data["end_time"] = str(datetime.now())

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

    print(f"Deploy finalizado. Log salvo em: {LOG_FILE}")

if __name__ == "__main__":
    print("Iniciando deploy automático do MindScan...")
    deploy_all()
    print("Deploy concluído com sucesso.")
