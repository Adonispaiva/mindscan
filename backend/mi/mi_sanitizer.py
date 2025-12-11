# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_sanitizer.py
# Última atualização: 2025-12-11T09:59:20.872348

from __future__ import annotations
from typing import Dict, Any


class MISanitizer:
    """
    Sanitiza dados de entrada e saída:
    - remove campos desnecessários
    - padroniza tipos
    - garante compatibilidade entre módulos
    """

    def clean(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        clean_data = {}

        for key, value in payload.items():
            if value is None:
                continue
            if isinstance(value, str):
                clean_data[key] = value.strip()
            else:
                clean_data[key] = value

        return clean_data
