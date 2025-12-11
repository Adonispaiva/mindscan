# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\persona\persona_constraints.py
# Última atualização: 2025-12-11T09:59:20.943725

from __future__ import annotations
from typing import Dict, Any


class PersonaConstraints:
    """
    Define restrições estruturais e de segurança da persona interna.
    Evita:
    - contradições entre módulos
    - estilos inadequados
    - quebras de coerência narrativa
    """

    def validate(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        issues = {}

        if "voice" not in profile:
            issues["voice"] = "Persona sem voz definida."

        if "style" not in profile:
            issues["style"] = "Estilo textual não especificado."

        # Checagens de sabotagem narrativa
        forbidden = ["incongruente", "agressivo", "insensível"]
        if any(word in profile.get("style", "").lower() for word in forbidden):
            issues["style_flag"] = "Estilo contém elementos proibidos."

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
