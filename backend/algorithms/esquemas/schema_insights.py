# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\schema_insights.py
# Última atualização: 2025-12-11T09:59:20.683445

"""
Schema Insights
Gera interpretações qualitativas a partir das dimensões intermediárias
e dos 18 esquemas finais, oferecendo material para narrativa e relatórios.
"""

from typing import Dict


class SchemaInsights:
    """
    Produz insights psicodinâmicos com base nas intensidades observadas.
    """

    def __init__(self):
        self.version = "1.0"

        self.templates = {
            "abandono": "Sensibilidade extrema ao medo de perda e instabilidade.",
            "desconfianca": "Tendência a interpretar interações com suspeita.",
            "privacao_emocional": "Percepção crônica de falta de acolhimento.",
            "defectividade": "Autoimagem vulnerável a críticas e rejeição.",
            "isolamento": "Sentimento de desconexão social persistente.",
            "dependencia": "Necessidade intensa de apoio externo.",
            "vulnerabilidade": "Preocupações exageradas com riscos e ameaças.",
            "emaranhamento": "Dificuldade de estabelecer identidade própria.",
            "fracasso": "Crença de inadequação e baixa eficácia.",
            "submissao": "Supressão de necessidades para evitar conflitos.",
            "autossacrificio": "Doação excessiva que leva à exaustão emocional.",
            "busca_aprovacao": "Alta dependência da validação externa.",
            "negatividade": "Foco desproporcional em aspectos negativos.",
            "inibicao_emocional": "Supressão rígida de emoções e impulsos.",
            "hipercriticismo": "Autoexigência intensa e perfeccionismo.",
            "direitos_especiais": "Busca por favorecimento e exceções.",
            "autocontrole_insuficiente": "Dificuldade em frear impulsos.",
            "padrões_inflexíveis": "Rigidez e dificuldade de adaptação.",
        }

    def generate(self, classified: Dict[str, float]) -> Dict[str, str]:
        """
        Insights são gerados para esquemas com intensidade mínima de 40.
        """

        insights = {}

        for schema, value in classified.items():
            if value >= 40:
                insights[schema] = self.templates.get(
                    schema,
                    "Padrão psicológico significativo observado nesta área."
                )

        return insights
