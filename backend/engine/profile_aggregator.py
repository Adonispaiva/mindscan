# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\profile_aggregator.py
# Última atualização: 2025-12-11T09:59:20.824000

"""
MindScan — Profile Aggregator
Inovexa Software — Engenharia Ultra Superior

Une múltiplos perfis oriundos de módulos como:
- Big Five
- DASS
- TEIQue
- OCAI
- Cruzamentos

Garante coerência e define o perfil psicológico final.
"""

from typing import Dict, Any, List


class ProfileAggregator:
    def __init__(self):
        self.profiles: List[Dict[str, Any]] = []

    def add_profile(self, profile: Dict[str, Any]):
        self.profiles.append(profile)

    def consolidate(self) -> Dict[str, Any]:
        """Consolida os perfis em um perfil primário final."""

        merged = {}
        for p in self.profiles:
            for k, v in p.items():
                merged[k] = v  # último perfil sobrepõe anteriores

        # Determina “primary” se existir
        primary = merged.get("primary", None)

        return {
            "profile": merged,
            "primary": primary,
            "engine": "ProfileAggregator"
        }
