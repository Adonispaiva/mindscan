# ================================================================
#  MINDSCAN — TEIQue — ALERTS ENGINE
#  Autor: Leo Vinci (Inovexa)
#
#  Objetivo:
#     Gerar alertas emocionais e interpessoais derivados dos
#     níveis das facetas do modelo TEIQue (Trait Emotional Intelligence).
#
#  Usado por:
#     - teique_insights
#     - teique_summary
#     - cross_teique_*
#     - PDF (inteligência emocional)
#
#  Estrutura:
#     get_teique_alerts(profile) → retorna alertas por faceta
# ================================================================

from typing import Dict, List


# ---------------------------------------------------------------
#  ALERTAS PRINCIPAIS POR FACETA
# ---------------------------------------------------------------
TEIQUE_ALERT_MATRIX = {
    "Bem-Estar": {
        "high": [
            "Confiança emocional elevada pode gerar subestimação de riscos.",
            "Otimismo excessivo em situações de incerteza."
        ],
        "low": [
            "Baixa percepção de autoeficácia emocional.",
            "Possível vulnerabilidade a frustrações."
        ]
    },

    "Autocontrole": {
        "high": [
            "Alto controle emocional pode dificultar expressão afetiva.",
            "Risco de repressão emocional em contextos de conflito."
        ],
        "low": [
            "Dificuldade em regular impulsos emocionais.",
            "Aumento de reações intempestivas sob estresse."
        ]
    },

    "Emocionalidade": {
        "high": [
            "Sensibilidade emocional elevada pode gerar sobrecarga afetiva.",
            "Risco de ruminação emocional."
        ],
        "low": [
            "Baixa responsividade emocional pode afetar vínculos afetivos.",
            "Percepção limitada de nuances emocionais."
        ]
    },

    "Sociabilidade": {
        "high": [
            "Busca constante por aprovação social.",
            "Dependência de estímulos sociais para validação."
        ],
        "low": [
            "Isolamento emocional ou baixa interação positiva.",
            "Dificuldade em buscar suporte emocional."
        ]
    }
}


# ---------------------------------------------------------------
#  FUNÇÃO PRINCIPAL
# ---------------------------------------------------------------
def get_teique_alerts(levels: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Gera alertas emocionais e interpessoais com base nos níveis:

    Exemplo:
        {
            "Bem-Estar": "high",
            "Autocontrole": "low",
            ...
        }
    """

    alerts = {}

    for facet, level in levels.items():
        if facet in TEIQUE_ALERT_MATRIX and level in ("high", "low"):
            alerts[facet] = TEIQUE_ALERT_MATRIX[facet][level]

    return alerts


# ---------------------------------------------------------------
#  TESTE LOCAL
# ---------------------------------------------------------------
if __name__ == "__main__":
    sample = {
        "Bem-Estar": "low",
        "Autocontrole": "high",
        "Emocionalidade": "low",
        "Sociabilidade": "medium"
    }

    out = get_teique_alerts(sample)
    print("TEIQUE ALERTS:", out)
