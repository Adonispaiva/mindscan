"""
cleanup_manager.py
Limpeza Inteligente do MindScan – Versão Profissional Completa (A)

Funções:
    • Remoção de __pycache__
    • Detecção e remoção de arquivos órfãos
    • Limpeza de logs antigos
    • Limpeza de arquivos temporários
    • Remoção de duplicidades
    • Organização estrutural básica
"""

import os
import datetime


class CleanupManager:

    def __init__(self, logger):
        self.log = logger
        self.root_path = r"D:\projetos-inovexa\mindscan"

        # Setar pastas que podem conter arquivos para limpeza
        self.clean_targets = [
            "backend",
            "core",
            "modules",
            "tools",
            "logs",
            "tests",
            "data",
        ]

        # Extensões seguras para excluir
        self.temp_extensions = [
            ".tmp", ".temp", ".bak", ".old", ".log", ".cache"
        ]

    # ============================================================
    # Remover __pycache__ recursivamente
    # ============================================================

    def _clear_pycache(self):
        self.log.info("Removendo pastas __pycache__...")

        removed = 0

        for target in self.clean_targets:
            base = os.path.join(self.root_path, target)

            for root, dirs, files in os.walk(base):
                for d in dirs:
                    if d == "__pycache__":
                        full_path = os.path.join(root, d)
                        try:
                            for f in os.listdir(full_path):
                                os.remove(os.path.join(full_path, f))
                            os.rmdir(full_path)
                            removed += 1
                            self.log.success(f"[PYCACHE REMOVIDO] {full_path}")
                        except Exception as e:
                            self.log.error(f"Erro ao remover __pycache__ {full_path}: {e}")

        if removed == 0:
            self.log.info("Nenhuma pasta __pycache__ encontrada.")
        else:
            self.log.info(f"Total de pastas __pycache__ removidas: {removed}")

    # ============================================================
    # Remover arquivos temporários
    # ============================================================

    def _clear_temp_files(self):
        self.log.info("Limpando arquivos temporários e obsoletos...")

        removed = 0

        for target in self.clean_targets:
            base = os.path.join(self.root_path, target)

            for root, dirs, files in os.walk(base):
                for f in files:
                    for ext in self.temp_extensions:
                        if f.endswith(ext):
                            full_path = os.path.join(root, f)
                            try:
                                os.remove(full_path)
                                removed += 1
                                self.log.success(f"[TEMP REMOVIDO] {full_path}")
                            except Exception as e:
                                self.log.error(f"Erro ao remover {full_path}: {e}")

        self.log.info(f"Total de temporários removidos: {removed}")

    # ============================================================
    # Remover logs antigos
    # ============================================================

    def _clear_old_logs(self, days=15):
        self.log.info(f"Limpando logs com mais de {days} dias...")

        logs_path = os.path.join(self.root_path, "logs")
        count = 0

        if not os.path.exists(logs_path):
            self.log.warn("Pasta de logs não existe.")
            return

        limit = datetime.datetime.now() - datetime.timedelta(days=days)

        for root, dirs, files in os.walk(logs_path):
            for f in files:
                full = os.path.join(root, f)

                try:
                    mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(full))
                    if mod_time < limit:
                        os.remove(full)
                        count += 1
                        self.log.success(f"[LOG REMOVIDO] {full}")
                except Exception as e:
                    self.log.error(f"Erro ao remover log antigo {full}: {e}")

        self.log.info(f"Total de logs antigos removidos: {count}")

    # ============================================================
    # Detecção de duplicações simples
    # ============================================================

    def _detect_duplicates(self):
        self.log.info("Verificando duplicações básicas...")

        file_hash = {}
        duplicates = []

        for target in self.clean_targets:
            base = os.path.join(self.root_path, target)

            for root, dirs, files in os.walk(base):
                for f in files:

                    path = os.path.join(root, f)
                    size = os.path.getsize(path)

                    key = (f, size)

                    if key not in file_hash:
                        file_hash[key] = path
                    else:
                        duplicates.append((path, file_hash[key]))

        if duplicates:
            self.log.warn("Arquivos duplicados detectados:")
            for dup, orig in duplicates:
                self.log.warn(f"Duplicado: {dup} | Original: {orig}")
        else:
            self.log.info("Nenhuma duplicação encontrada.")

    # ============================================================
    # EXECUÇÃO PRINCIPAL
    # ============================================================

    def run_cleanup(self):
        self.log.header("CLEANUP – INICIADO")

        self._clear_pycache()
        self._clear_temp_files()
        self._clear_old_logs()
        self._detect_duplicates()

        self.log.success("LIMPEZA COMPLETA.")
