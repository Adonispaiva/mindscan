# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\big5\big5_crosslinks.py
# Última atualização: 2025-12-11T09:59:20.596784

"""
Big5 Crosslinks — Versão Ultra Superior
---------------------------------------

Conecta dimensões Big Five com:
- Performance
- TEIQue (Inteligência Emocional)
- Estilos mentais
- Cultura organizacional (OCAI)
- Fatores de risco e força

Este módulo funciona como “ponte semântica” do MindScan.
"""

from typing import Dict, Any


class Big5Crosslinks:
    def __init__(self):
        self.version = "2.0-ultra"

        # Relacionamentos principais entre Big5 → Performance
        self.performance_links = {
            "conscienciosidade": "Aumenta consistência, confiabilidade e precisão na execução.",
            "abertura": "Potencializa inovação e adaptabilidade em ambientes dinâmicos.",
            "extroversao": "Eleva influência, energia social e comunicação ativa.",
            "amabilidade": "Aprimora trabalho em equipe, mediação e colaboração.",
            "neuroticismo": "Impacta estabilidade emocional e tolerância a pressão.",
        }

        # Links Big5 → TEIQue
        self.emotional_links = {
            "neuroticismo": "Relaciona-se à autorregulação emocional e resiliência.",
            "amabilidade": "Contribui para empatia, percepção interpessoal e vínculos.",
            "extroversao": "Apoia expressividade emocional e presença social.",
        }

        # Links Big5 → Cultura (OCAI)
        self.culture_links = {
            "abertura": "Relacionada à Adhocracia (inovação, experimentação).",
            "conscienciosidade": "Relacionada à Hierarquia (ordem, estabilidade).",
            "extroversao": "Relacionada ao Mercado (dinamismo, assertividade).",
            "amabilidade": "Relacionada ao Clã (colaboração, suporte humano).",
        }

    def generate(self, dims: Dict[str, float]) -> Dict[str, Any]:
        cross = {
            "performance": {},
            "emocional": {},
            "cultura": {},
        }

        for dim, value in dims.items():
            if value >= 40:
                if dim in self.performance_links:
                    cross["performance"][dim] = self.performance_links[dim]

                if dim in self.emotional_links:
                    cross["emocional"][dim] = self.emotional_links[dim]

                if dim in self.culture_links:
                    cross["cultura"][dim] = self.culture_links[dim]

        return {
            "module": "Big5",
            "version": self.version,
            "crosslinks": cross,
        }
