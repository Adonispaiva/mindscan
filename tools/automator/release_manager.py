"""
release_manager.py
Gerador Profissional de Releases do MindScan
Versão Profissional Completa (A)

Funções:
    • Criar pacote ZIP oficial do projeto
    • Incluir backend, core, modules, tools/automator e logs essenciais
    • Criar metadados da release
    • Organizar diretório de releases
"""

import os
import zipfile
import datetime
import json


class ReleaseManager:

    def __init__(self, logger):
        self.log = logger
        self.root_path = r"D:\projetos-inovexa\mindscan"
        self.releases_dir = os.path.join(self.root_path, "releases")

        os.makedirs(self.releases_dir, exist_ok=True)

    # ============================================================
    # Criar metadados da release
    # ============================================================

    def _create_metadata(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        metadata = {
            "project": "MindScan",
            "version": timestamp.replace(":", "-").replace(" ", "_"),
            "generated_at": timestamp,
            "paths_included": [
                "backend",
                "core",
                "modules",
                "tools/automator",
                "logs"
            ],
            "generator": "MindScan Automator – ReleaseManager"
        }

        return metadata

    # ============================================================
    # Função auxiliar para adicionar pastas no ZIP
    # ============================================================

    def _add_folder_to_zip(self, zipf, folder_path, zip_root):
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                full_path = os.path.join(root, f)
                relative_path = os.path.relpath(full_path, folder_path)
                arcname = os.path.join(zip_root, relative_path)
                zipf.write(full_path, arcname)
                self.log.info(f"[ADD] {arcname}")

    # ============================================================
    # Execução principal
    # ============================================================

    def generate_release(self):
        self.log.header("RELEASE BUILDER – INICIADO")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        release_name = f"mindscan_release_{timestamp}.zip"
        release_path = os.path.join(self.releases_dir, release_name)

        metadata = self._create_metadata()

        self.log.info(f"Criando release: {release_path}")

        # Criar ZIP
        with zipfile.ZipFile(release_path, "w", zipfile.ZIP_DEFLATED) as zipf:

            # Adicionar metadados
            meta_path = os.path.join(self.releases_dir, f"metadata_{timestamp}.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)

            zipf.write(meta_path, f"metadata.json")
            self.log.success("Metadados incluídos.")

            # Adicionar pastas principais
            folders = [
                ("backend", "backend"),
                ("core", "core"),
                ("modules", "modules"),
                ("tools/automator", "tools/automator"),
                ("logs", "logs"),
            ]

            for folder, zip_root in folders:
                abs_path = os.path.join(self.root_path, folder)
                if os.path.exists(abs_path):
                    self.log.info(f"Adicionando pasta ao pacote: {folder}")
                    self._add_folder_to_zip(zipf, abs_path, zip_root)
                else:
                    self.log.warn(f"Pasta ausente, ignorada: {folder}")

        self.log.success(f"RELEASE GERADA:\n{release_path}")
        return True
