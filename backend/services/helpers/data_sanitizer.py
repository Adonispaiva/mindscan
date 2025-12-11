# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\helpers\data_sanitizer.py
# Última atualização: 2025-12-11T09:59:21.152631

# -*- coding: utf-8 -*-
"""
data_sanitizer.py
-----------------

Sanitiza o payload, garantindo consistência e ausência de ruídos.
"""

from typing import Dict, Any


class DataSanitizer:

    @staticmethod
    def sanitize(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normaliza dados para evitar falhas no pipeline.
        """
        cleaned = {}

        for key, value in payload.items():
            if isinstance(value, str):
                cleaned[key] = value.strip()
            else:
                cleaned[key] = value

        return cleaned
