# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_dialogue_coach.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIDialogueCoach:
    """
    Sugere diálogos de coaching com base nos padrões comportamentais detectados.
    """

    @staticmethod
    def coach(results: dict) -> list:
        prompts = []

        if results.get("performance_estimate", 50) < 50:
            prompts.append("Quais obstáculos você percebe na sua execução diária?")

        if results.get("risks", {}):
            prompts.append("Que situações mais exigem seu autocontrole emocional?")

        if results.get("semantic", {}):
            prompts.append("Como suas competências se manifestam no ambiente atual?")

        return prompts
