# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\teique\teique_crosslinks.py
# Última atualização: 2025-12-11T09:59:20.714601

# ================================================================
#  MINDSCAN — TEIQue — CROSSLINKS ENGINE
#  Autor: Leo Vinci (Inovexa)
#
#  Objetivo:
#     Consolidar interações cruzadas entre as quatro grandes
#     facetas do TEIQue:
#         - Bem-Estar
#         - Autocontrole
#         - Emocionalidade
#         - Sociabilidade
#
#     Essas interações são usadas para:
#         - Insights
#         - Recomendações
#         - Cruzamentos (cross modules)
#         - PDF (Inteligência Emocional)
#
#  Estrutura:
#     get_teique_crosslinks(profile) → retorna padrões combinados
# ================================================================

from typing import Dict, List


# ---------------------------------------------------------------
#  MATRIZ DE INTERAÇÕES CRUZADAS DO TEIQUE
# ---------------------------------------------------------------
TEIQUE_CROSS_MATRIX = {
    ("Bem-Estar", "Autocontrole"): {
        ("high", "low"): [
            "Alta confiança emocional com baixa regulação → risco de impulsividade otimista.",
            "Pode tomar decisões rápidas sem avaliar consequências."
        ],
        ("low", "high"): [
            "Baixo bem-estar com alto autocontrole → tendência a supressão emocional.",
            "Risco de rigidez afetiva."
        ]
    },

    ("Bem-Estar", "Emocionalidade"): {
        ("high", "high"): [
            "Otimismo elevado combinado com sensibilidade emocional intensa.",
            "Perfil emocionalmente expansivo, mas vulnerável à sobrecarga."
        ],
        ("low", "low"): [
            "Retraimento emocional com baixa autoconfiança.",
            "Risco de desmotivação profunda."
        ]
    },

    ("Autocontrole", "Emocionalidade"): {
        ("high", "high"): [
            "Controle alto sobre emoções intensas → possível tensão interna.",
            "Risco de acúmulo emocional antes de eventual explosão."
        ],
        ("low", "high"): [
            "Reatividade emocional com baixa regulação.",
            "Alta vulnerabilidade a estímulos de estresse."
        ]
    },

    ("Sociabilidade", "Bem-Estar"): {
        ("high", "low"): [
            "Busca social elevada apesar de baixa autoconfiança.",
            "Possível dependência emocional de validação externa."
        ],
        ("low", "high"): [
            "Autossuficiência emocional com baixa necessidade social.",
            "Perfil mais individualista e introspectivo."
        ]
    },

    ("Sociabilidade", "Autocontrole"): {
        ("high", "low"): [
            "Extroversão emocional com baixa regulação.",
            "Risco de impulsividade social."
        ],
        ("low", "high"): [
            "Controle elevado com baixa sociabilidade.",
            "Perfil introspectivo e reservado."
        ]
    }
}


# ---------------------------------------------------------------
#  FUNÇÃO PRINCIPAL
# ---------------------------------------------------------------
def get_teique_crosslinks(levels: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Gera interações cruzadas entre as facetas TEIQue.
    """

    result = {}

    facets = list(levels.keys())

    for i in range(len(facets)):
        for j in range(i + 1, len(facets)):
            f1, f2 = facets[i], facets[j]
            lvl1, lvl2 = levels.get(f1), levels.get(f2)

            key = (f1, f2)
            key_rev = (f2, f1)

            combo = (lvl1, lvl2)
            combo_rev = (lvl2, lvl1)

            # Direção normal
            if key in TEIQUE_CROSS_MATRIX:
                if combo in TEIQUE_CROSS_MATRIX[key]:
                    result.setdefault(f"{f1}-{f2}", [])
                    result[f"{f1}-{f2}"].extend(TEIQUE_CROSS_MATRIX[key][combo])

            # Direção invertida
            if key_rev in TEIQUE_CROSS_MATRIX:
                if combo_rev in TEIQUE_CROSS_MATRIX[key_rev]:
                    result.setdefault(f"{f1}-{f2}", [])
                    result[f"{f1}-{f2}"].extend(TEIQUE_CROSS_MATRIX[key_rev][combo_rev])

    return result


# ---------------------------------------------------------------
#  TESTE LOCAL
# ---------------------------------------------------------------
if __name__ == "__main__":
    sample = {
        "Bem-Estar": "high",
        "Autocontrole": "low",
        "Emocionalidade": "high",
        "Sociabilidade": "low"
    }

    out = get_teique_crosslinks(sample)
    print("TEIQUE CROSSLINKS:", out)
