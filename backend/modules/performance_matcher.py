# ===============================================================
#  MÓDULO: PERFORMANCE MATCHER
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Determinar o quadrante da Bússola de Talentos com base
#          em indicadores de performance e perfil emocional.
# ===============================================================

from typing import Dict

def calcular_matcher(dados: Dict) -> Dict:
    """
    Calcula o quadrante da Bússola de Talentos SynMind com base em
    indicadores de performance, excelência e fatores emocionais.

    Parâmetros:
        dados = {
            "excelencia": float (0-100),
            "faturamento": float (0-100),
            "scores": {"DEPRESSAO": int, "ANSIEDADE": int, "ESTRESSE": int}
        }

    Retorna:
        {
            "quadrante": str,
            "score_performance": float,
            "comentario": str
        }
    """

    excelencia = float(dados.get("excelencia", 50))
    faturamento = float(dados.get("faturamento", 50))
    scores = dados.get("scores", {})

    depressao = scores.get("DEPRESSAO", 0)
    ansiedade = scores.get("ANSIEDADE", 0)
    estresse = scores.get("ESTRESSE", 0)

    # ----------------------------------------
    # Cálculo base de performance e equilíbrio
    # ----------------------------------------
    emocional = max(0, 100 - ((depressao + ansiedade + estresse) / 3) * 3.3)
    score_performance = round((excelencia * 0.6 + faturamento * 0.4) * (emocional / 100), 2)

    # ----------------------------------------
    # Determinação do quadrante (Bússola)
    # ----------------------------------------
    if excelencia >= 70 and faturamento >= 70:
        quadrante = "Inspirador"
        comentario = (
            "Alta excelência e alta entrega. "
            "Você atua com propósito e visão sistêmica — o verdadeiro líder inspirador."
        )
    elif excelencia >= 70 and faturamento < 70:
        quadrante = "Especialista"
        comentario = (
            "Alta excelência técnica com foco interno. "
            "Seu domínio técnico é excepcional, ideal para papéis de profundidade."
        )
    elif excelencia < 70 and faturamento >= 70:
        quadrante = "Promissor"
        comentario = (
            "Alta entrega e aprendizado rápido. "
            "Seu foco em resultados te projeta para crescimento acelerado."
        )
    else:
        quadrante = "Buscador"
        comentario = (
            "Fase de desenvolvimento e autoconhecimento. "
            "Você está estruturando competências para alcançar constância."
        )

    return {
        "quadrante": quadrante,
        "score_performance": score_performance,
        "comentario": comentario
    }


# ---------------------------------------------------------------
# Função utilitária: gerar texto de análise resumida
# ---------------------------------------------------------------
def gerar_analise_performance(resultados: Dict) -> str:
    """
    Gera um resumo textual do quadrante e score de performance.
    """
    q = resultados.get("quadrante")
    sp = resultados.get("score_performance")
    comentario = resultados.get("comentario")

    return f"""
📊 RESULTADO SYNMIND PERFORMANCE
Quadrante: {q}
Score Geral de Performance: {sp}%
Comentário: {comentario}
"""
