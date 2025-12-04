"""
CROSS OCAI × DASS21 — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona indicadores de estresse, ansiedade e depressão (DASS21)
com o modelo de cultura organizacional OCAI:

- Clã (colaboração)
- Adocracia (inovação)
- Mercado (competição)
- Hierarquia (estrutura)

Objetivo:
Detectar incompatibilidades entre estado psicológico e cultura.
"""

from typing import Dict, Any


class CrossOCAIDASS:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, ocai: Dict[str, float], dass: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # Estresse alto × Cultura competitiva
        if dass.get("stress", 0) >= 60 and ocai.get("mercado", 0) >= 55:
            patterns["risco_burnout_mercado"] = (
                "Ambiente competitivo pode intensificar estresse elevado."
            )

        # Depressão × Cultura colaborativa (choque de suporte emocional)
        if dass.get("depressao", 0) >= 55 and ocai.get("clan", 0) >= 55:
            patterns["desalinhamento_suporte"] = (
                "Depressão elevada pode prejudicar envolvimento em culturas colaborativas."
            )

        # Ansiedade × Inovação
        if dass.get("ansiedade", 0) >= 60 and ocai.get("inovacao", 0) >= 55:
            patterns["ansiedade_ambiente_dinamico"] = (
                "Ambientes de alta mudança podem acentuar sintomas de ansiedade."
            )

        # Stress + Hierarquia (pode funcionar como estabilizador)
        if dass.get("stress", 0) >= 55 and ocai.get("hierarquia", 0) >= 60:
            patterns["estrutura_estabilizadora"] = (
                "Apesar do estresse, ambientes estruturados podem oferecer previsibilidade."
            )

        return {
            "module": "cross_ocai_dass",
            "version": self.version,
            "patterns": patterns,
        }
