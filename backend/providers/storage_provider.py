# ============================================================
# MindScan — Storage Provider
# ============================================================
# Provedor unificado para armazenamento de arquivos e objetos.
#
# Responsável por:
# - salvar arquivos locais
# - carregar arquivos
# - excluir arquivos
# - criar diretórios automaticamente
# - servir como ponte futura para:
#       • AWS S3
#       • Azure Blob
#       • Google Cloud Storage
#
# Versão: Final — SynMind 2025
# ============================================================

import os
from typing import Optional, List


class StorageProvider:
    """
    Provedor de armazenamento de arquivos do MindScan.
    """

    def __init__(self, base_path: str = "storage"):
        self.base_path = base_path
        self._ensure_directory(self.base_path)

    # ------------------------------------------------------------
    # Garantir pasta
    # ------------------------------------------------------------
    def _ensure_directory(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    # ------------------------------------------------------------
    # Caminho absoluto
    # ------------------------------------------------------------
    def _full_path(self, filename: str) -> str:
        return os.path.join(self.base_path, filename)

    # ------------------------------------------------------------
    # Salvar arquivo
    # ------------------------------------------------------------
    def save(self, filename: str, content: bytes) -> str:
        full_path = self._full_path(filename)
        directory = os.path.dirname(full_path)
        self._ensure_directory(directory)

        with open(full_path, "wb") as f:
            f.write(content)

        return full_path

    # ------------------------------------------------------------
    # Carregar arquivo
    # ------------------------------------------------------------
    def load(self, filename: str) -> Optional[bytes]:
        full_path = self._full_path(filename)

        if not os.path.exists(full_path):
            return None

        with open(full_path, "rb") as f:
            return f.read()

    # ------------------------------------------------------------
    # Excluir arquivo
    # ------------------------------------------------------------
    def delete(self, filename: str) -> bool:
        full_path = self._full_path(filename)

        if os.path.exists(full_path):
            os.remove(full_path)
            return True

        return False

    # ------------------------------------------------------------
    # Listar arquivos
    # ------------------------------------------------------------
    def list(self) -> List[str]:
        result = []

        for root, _, files in os.walk(self.base_path):
            for f in files:
                result.append(os.path.join(root, f))

        return result
