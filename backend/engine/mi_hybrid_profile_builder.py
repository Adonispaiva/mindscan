# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\mi_hybrid_profile_builder.py
# Última atualização: 2025-12-11T09:59:20.816999

# ============================================================
# MindScan — MI Hybrid Profile Builder
# ============================================================
# Constrói um perfil híbrido consolidado a partir:
# - Normalized blocks
# - Reasoning
# - Persona
# - MI Clássico + Avançado + SynMind
#
# Entregável final:
#   Estrutura única coerente para renderização PDF e API.
# ============================================================

from typing import Dict, Any


class MIHybridProfileBuilder:

    def __init__(self):
        pass

    def build(self, hybrid_output: Dict[str, Any]) -> Dict[str, Any]:

        engine_used = hybrid_output.get("engine")
        insights = hybrid_output.get("payload", {}).get("insights", {})
        persona = hybrid_output.get("payload", {}).get("persona", {})
        normalized = hybrid_output.get("payload", {}).get("normalized", {})

        profile = {
            "engine_used": engine_used,
            "persona_identity": persona.get("core", {}),
            "persona_style": persona.get("style", {}),
            "persona_voice": persona.get("voice", {}),

            "insights": insights,
            "normalized": normalized,

            "metadata": {
                "profile_version": "hybrid.1.0",
                "origin": engine_used,
            }
        }

        return profile
