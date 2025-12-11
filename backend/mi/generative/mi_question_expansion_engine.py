# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_question_expansion_engine.py
# Última atualização: 2025-12-11T09:59:20.929428

class MIQuestionExpansionEngine:
    """
    Sugere novas perguntas para aprofundar o diagnóstico
    com base nos padrões detectados.
    """

    @staticmethod
    def suggest(results: dict) -> list:
        suggestions = []

        if results.get("risks", {}):
            suggestions.append("Como você lida com situações de pressão inesperada?")

        if results.get("performance_estimate", 50) < 50:
            suggestions.append("O que mais dificulta sua consistência operacional?")

        if results.get("semantic", {}):
            suggestions.append("Como você percebe sua colaboração dentro de equipes diversas?")

        return suggestions
