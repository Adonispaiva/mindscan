# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\persona\persona_filters.py
# Última atualização: 2025-12-11T09:59:20.946732

from __future__ import annotations
from typing import Dict, Any


class PersonaFilters:
    """
    Filtra elementos inadequados na comunicação da persona.
    """

    def apply(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        filtered = {}

        blocked_terms = ["diagnóstico", "doença", "tratamento"]
        replacements = {"diagnóstico": "avaliação", "doença": "condição", "tratamento": "acompanhamento"}

        for key, value in payload.items():
            if isinstance(value, str):
                text = value
                for term in blocked_terms:
                    if term in text.lower():
                        text = text.replace(term, replacements[term])
                filtered[key] = text
            else:
                filtered[key] = value

        return filtered
