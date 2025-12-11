# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_assets.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
report_assets.py
----------------

Centraliza o acesso a recursos visuais, logos, fontes e assets utilizados
nos relatórios do MindScan Corporate.
"""

import base64
import os


class ReportAssets:

    BASE_DIR = "assets/report"

    @staticmethod
    def get_asset_path(filename: str) -> str:
        """
        Retorna o caminho absoluto para um asset.
        """
        path = os.path.join(ReportAssets.BASE_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Asset não encontrado: {path}")
        return path

    @staticmethod
    def load_base64(filename: str) -> str:
        """
        Carrega um asset (logo, ícone) como base64 para embutir no HTML.
        """
        path = ReportAssets.get_asset_path(filename)

        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{data}"
