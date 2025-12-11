# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\big5\big5_insights.py
# Última atualização: 2025-12-11T09:59:20.600842

"""
Big5 Insights — Versão Ultra Superior
-------------------------------------

Gera insights semânticos aprofundados para cada uma das
cinco dimensões da personalidade segundo o modelo Big Five.

Melhorias:
- Insights condicionais por intensidade
- Classificação de padrões
- Descrições avançadas para relatórios MindScan
- Robustez contra dados incompletos
"""

from typing import Dict


class Big5Insights:
    def __init__(self):
        self.version = "2.0-ultra"

        self.templates = {
            "abertura": {
                "alta": "Alta abertura indica criatividade, flexibilidade cognitiva e forte curiosidade intelectual.",
                "media": "Abertura moderada sugere curiosidade equilibrada e adaptabilidade sem excessos.",
                "baixa": "Baixa abertura sugere preferência por rotinas, práticas estáveis e menor busca por novidades."
            },
            "conscienciosidade": {
                "alta": "Alta conscienciosidade reflete organização, disciplina e foco em resultados.",
                "media": "Conscienciosidade moderada sugere consistência com espaço para melhoria previsível.",
                "baixa": "Baixa conscienciosidade indica menor organização e possíveis variações de produtividade."
            },
            "extroversao": {
                "alta": "Alta extroversão aponta sociabilidade intensa, assertividade e energia elevada.",
                "media": "Extroversão moderada combina sociabilidade funcional com foco equilibrado.",
                "baixa": "Baixa extroversão indica introspecção, profundidade analítica e preferência por interações seletivas."
            },
            "amabilidade": {
                "alta": "Alta amabilidade revela empatia, colaboração e relacionamento harmonioso.",
                "media": "Amabilidade moderada indica flexibilidade social sem perda de autonomia.",
                "baixa": "Baixa amabilidade sugere assertividade elevada e possível foco em resultados sobre relações."
            },
            "neuroticismo": {
                "alta": "Neuroticismo elevado sugere sensibilidade emocional intensa e reatividade.",
                "media": "Nível moderado indica percepção emocional ativa porém equilibrada.",
                "baixa": "Neuroticismo baixo reflete estabilidade emocional e resistência ao estresse."
            }
        }

    def _zone(self, value: float) -> str:
        if value >= 70:
            return "alta"
        if value >= 40:
            return "media"
        return "baixa"

    def generate(self, dims: Dict[str, float]) -> Dict[str, str]:
        insights = {}

        for dim, value in dims.items():
            zone = self._zone(value)
            insight = self.templates.get(dim, {}).get(zone)
            if insight:
                insights[dim] = insight

        return insights
