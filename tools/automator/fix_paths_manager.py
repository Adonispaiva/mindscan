import os
import json
import shutil
from datetime import datetime

TARGET_OLD = "mindscan"
TARGET_NEW = "mindscan"

class FixPathsManager:
    def __init__(self, root_path):
        self.root_path = root_path
        self.log_entries = []
        self.modified_files = []

    def _log(self, message):
        self.log_entries.append(message)
        print(message)

    def _create_backup(self, file_path):
        backup_dir = os.path.join(self.root_path, "backups_autofix")
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_file = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")

        shutil.copy2(file_path, backup_file)

    def _process_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if TARGET_OLD not in content:
                return

            # Backup
            self._create_backup(file_path)

            # Fix content
            updated_content = content.replace(TARGET_OLD, TARGET_NEW)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)

            self.modified_files.append(file_path)
            self._log(f"[FIXED] {file_path}")

        except Exception as e:
            self._log(f"[ERROR] {file_path}: {str(e)}")

    def run(self):
        self._log("=== AUTO-FIX MANAGER: INICIADO ===")

        for root, dirs, files in os.walk(self.root_path):
            for filename in files:
                if filename.lower().endswith((".py", ".txt", ".json", ".bat", ".ps1", ".md")):
                    file_path = os.path.join(root, filename)
                    self._process_file(file_path)

        # Gerar relatório
        report_dir = os.path.join(self.root_path, "logs/autofix")
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%Mmin%S")
        report_path = os.path.join(report_dir, f"autofix_{timestamp}.json")

        report_data = {
            "timestamp": timestamp,
            "root": self.root_path,
            "modified_files": self.modified_files,
            "total_modified": len(self.modified_files)
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4)

        self._log(f"=== AUTO-FIX MANAGER: CONCLUÍDO ===")
        self._log(f"Arquivos modificados: {len(self.modified_files)}")
        self._log(f"Relatório salvo em: {report_path}")
