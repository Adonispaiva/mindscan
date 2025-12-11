# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\utils\file_manager.py
# Última atualização: 2025-12-11T09:59:21.308202

# ============================================================
# MindScan — File Manager (UTILS)
# ============================================================
# Módulo responsável pelo gerenciamento completo de arquivos:
# - leitura e escrita segura
# - criação de diretórios
# - versionamento automático de arquivos
# - validação de caminhos
# - utilitário para exportações (PDF, JSON, models)
#
# Versão final e maximizada.
# ============================================================

import os
import json
from datetime import datetime
from typing import Any, Dict, Optional


class FileManager:
    """
    Gerenciador de arquivos do MindScan.
    Utilizado pelo:
    - Report Engine
    - MI Package Generator
    - Auditoria
    - Geradores de JSON
    """

    # ------------------------------------------------------------
    # CRIA DIRETÓRIO SE NÃO EXISTIR
    # ------------------------------------------------------------
    @staticmethod
    def ensure_dir(path: str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    # ------------------------------------------------------------
    # SALVAR JSON EM ARQUIVO
    # ------------------------------------------------------------
    @staticmethod
    def save_json(path: str, data: Dict[str, Any]):
        FileManager.ensure_dir(os.path.dirname(path))

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ------------------------------------------------------------
    # CARREGAR JSON
    # ------------------------------------------------------------
    @staticmethod
    def load_json(path: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ------------------------------------------------------------
    # SALVAR TEXTO GENÉRICO
    # ------------------------------------------------------------
    @staticmethod
    def save_text(path: str, content: str):
        FileManager.ensure_dir(os.path.dirname(path))

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    # ------------------------------------------------------------
    # LER TEXTO
    # ------------------------------------------------------------
    @staticmethod
    def load_text(path: str) -> Optional[str]:
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # ------------------------------------------------------------
    # VERSIONAMENTO AUTOMÁTICO
    # ------------------------------------------------------------
    @staticmethod
    def versioned_path(base_path: str) -> str:
        """
        Gera caminho versionado:
        example.pdf → example_2025-01-29_142300.pdf
        """
        root, ext = os.path.splitext(base_path)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
        return f"{root}_{timestamp}{ext}"

    # ------------------------------------------------------------
    # APAGAR ARQUIVO
    # ------------------------------------------------------------
    @staticmethod
    def delete(path: str):
        if os.path.exists(path):
            os.remove(path)

    # ------------------------------------------------------------
    # LISTAR ARQUIVOS EM DIRETÓRIO
    # ------------------------------------------------------------
    @staticmethod
    def list_files(path: str):
        if not os.path.exists(path):
            return []
        return os.listdir(path)
