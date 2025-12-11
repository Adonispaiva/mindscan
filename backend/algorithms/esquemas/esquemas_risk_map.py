# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas_risk_map.py
# Última atualização: 2025-12-11T09:59:20.683445

"""
Esquemas Risk Map
Gera o mapa de riscos clínicos baseado nos 18 Esquemas de Young.
"""

from typing import Dict


class EsquemasRiskMap:
    """
    Traduz pontuações elevadas em riscos psicodinâmicos específicos.
    """

    def __init__(self):
        self.version = "1.0"

        self.risk_map = {
            "abandono": "Risco de instabilidade relacional e medo intenso de perda.",
            "desconfianca": "Tendência a interpretar interações com suspeita.",
            "privacao_emocional": "Possível carência afetiva crônica.",
            "defectividade": "Autocrítica elevada e vulnerabilidade à vergonha.",
            "isolamento": "Isolamento social e baixa integração emocional.",
            "dependencia": "Dificuldade significativa de autonomia.",
            "vulnerabilidade": "Preocupação excessiva com segurança e ameaças.",
            "emaranhamento": "Dissolução de limites pessoais em relações próximas.",
            "fracasso": "Crença persistente de incapacidade.",
            "submissao": "Supressão de necessidades para evitar conflito.",
            "autossacrificio": "Negligência de si próprio em prol dos outros.",
            "busca_aprovacao": "Dependência da validação externa.",
            "negatividade": "Pessimismo acentuado e foco no lado negativo.",
            "inibicao_emocional": "Dificuldade de expressão emocional.",
            "hipercriticismo": "Autopressão intensa e perfeccionismo rígido.",
            "direitos_especiais": "Dificuldade em reconhecer limites externos.",
            "autocontrole_insuficiente": "Impulsividade e baixa tolerância à frustração.",
            "padrões_inflexíveis": "Rigidez cognitiva e emocional.",
        }

    def generate(self, classified: Dict[str, float]) -> Dict[str, str]:
        """
        Retorna riscos apenas para esquemas elevados (>70).
        """
        results = {}

        for schema, value in classified.items():
            if value >= 70:
                results[schema] = self.risk_map.get(
                    schema,
                    "Risco psicodinâmico associado ao esquema."
                )

        return results
