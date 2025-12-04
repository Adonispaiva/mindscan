"""
Big5 Risk Flags — Versão Ultra Superior
---------------------------------------

Gera FLAGS DE RISCO adicionais, diferentes do risk_map:
- risco de inconsistência
- risco de desequilíbrio dimensional
- risco de polarização extrema
- risco de volatilidade emocional

Este módulo aponta “alertas vermelhos” de personalidade.
"""

from typing import Dict, List


class Big5RiskFlags:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, dims: Dict[str, float]) -> List[str]:
        flags = []

        # 1) Polarização extrema
        for dim, value in dims.items():
            if value >= 90:
                flags.append(f"Atenção: {dim} em nível extremo pode gerar distorções comportamentais.")
            if value <= 10:
                flags.append(f"Possível deficiência crítica em {dim} — impacto funcional elevado.")

        # 2) Instabilidade emocional
        if dims.get("neuroticismo", 0) >= 75:
            flags.append("Risco elevado de instabilidade emocional e reatividade intensa.")

        # 3) Inconsistência dimensional
        gap = max(dims.values()) - min(dims.values()) if dims else 0
        if gap >= 60:
            flags.append("Perfil altamente assimétrico — grande variação entre dimensões.")

        return flags
