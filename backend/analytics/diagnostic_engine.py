from typing import Dict, Literal

# ---------------------------------------------
# 🧠 INTERPRETAÇÃO DO DASS-21
# ---------------------------------------------

DASS_LEVELS = {
    "DEPRESSAO": [(0, 9, "NORMAL"), (10, 13, "LEVE"), (14, 20, "MODERADO"), (21, 27, "GRAVE"), (28, 42, "EXTREMO")],
    "ANSIEDADE": [(0, 7, "NORMAL"), (8, 9, "LEVE"), (10, 14, "MODERADO"), (15, 19, "GRAVE"), (20, 42, "EXTREMO")],
    "ESTRESSE": [(0, 14, "NORMAL"), (15, 18, "LEVE"), (19, 25, "MODERADO"), (26, 33, "GRAVE"), (34, 42, "EXTREMO")],
}


def interpretar_nivel(valor: int, escala: str) -> str:
    for minimo, maximo, nivel in DASS_LEVELS[escala]:
        if minimo <= valor <= maximo:
            return nivel
    return "INDEFINIDO"


# ---------------------------------------------
# 🧩 ENGINE PRINCIPAL: interpretar_dass21()
# ---------------------------------------------
def interpretar_dass21(scores: Dict[str, int]) -> Dict[str, Dict[str, str]]:
    """
    Recebe um dicionário com escores do DASS-21 e retorna níveis + interpretação.
    Exemplo de entrada:
    {
        "DEPRESSAO": 6,
        "ANSIEDADE": 4,
        "ESTRESSE": 8
    }
    """
    resultado = {}
    for chave in ["DEPRESSAO", "ANSIEDADE", "ESTRESSE"]:
        raw_score = scores.get(chave, 0)
        nivel = interpretar_nivel(raw_score, chave)
        texto = gerar_interpretacao(chave, nivel)
        resultado[chave] = {
            "nivel": nivel,
            "score": str(raw_score),
            "texto": texto
        }
    return resultado


# ---------------------------------------------
# 📖 INTERPRETAÇÃO NARRATIVA
# ---------------------------------------------
def gerar_interpretacao(escala: Literal["DEPRESSAO", "ANSIEDADE", "ESTRESSE"], nivel: str) -> str:
    base = {
        "DEPRESSAO": {
            "NORMAL": "Não há indícios de sintomas depressivos clínicos.",
            "LEVE": "Sinais iniciais de desânimo, mas sem prejuízos graves.",
            "MODERADO": "Presença clara de tristeza e perda de interesse. Atenção recomendada.",
            "GRAVE": "Sintomas de depressão intensos. É recomendável acompanhamento clínico.",
            "EXTREMO": "Estado depressivo severo. Acompanhamento psicológico urgente é indicado."
        },
        "ANSIEDADE": {
            "NORMAL": "Níveis de ansiedade dentro da faixa esperada.",
            "LEVE": "Leve apreensão ou inquietação, sem impacto funcional.",
            "MODERADO": "Ansiedade perceptível com sintomas fisiológicos. Atenção sugerida.",
            "GRAVE": "Ansiedade significativa com possível interferência no cotidiano.",
            "EXTREMO": "Alta ansiedade com sofrimento intenso. Suporte clínico é recomendado."
        },
        "ESTRESSE": {
            "NORMAL": "A resposta ao estresse está regulada e funcional.",
            "LEVE": "Pequenos sinais de tensão, geralmente autogerenciáveis.",
            "MODERADO": "Carga de estresse perceptível, com risco de desgaste contínuo.",
            "GRAVE": "Estresse elevado com impacto emocional ou físico evidente.",
            "EXTREMO": "Sobrecarga severa. Intervenções de regulação são prioritárias."
        }
    }
    return base.get(escala, {}).get(nivel, "")
