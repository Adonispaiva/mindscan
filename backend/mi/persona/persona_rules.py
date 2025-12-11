# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\persona\persona_rules.py
# Última atualização: 2025-12-11T09:59:20.948776

from __future__ import annotations
from typing import Dict, Any


class PersonaRules:
    """
    Conjunto de regras que governam o comportamento textual da persona.
    São aplicadas antes da renderização final da resposta.
    """

    def apply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        rules_applied = {}

        for key, value in data.items():
            # Regra 1: nenhuma afirmação absoluta
            if isinstance(value, str):
                if "sempre" in value.lower():
                    value = value.replace("sempre", "normalmente")

                if "nunca" in value.lower():
                    value = value.replace("nunca", "raramente")

            rules_applied[key] = value

        # Regra 2: reforço de neutralidade
        rules_applied["neutralidade"] = True

        return rules_applied
