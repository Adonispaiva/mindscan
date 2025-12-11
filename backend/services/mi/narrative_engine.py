# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\mi\narrative_engine.py
# Última atualização: 2025-12-11T09:59:21.164629

class NarrativeEngine:
    """
    Gera narrativas brutas com base nos resultados psicométricos.
    Não aplica estilo nem compliance; isso é feito depois.
    """

    def __init__(self, results):
        self.results = results

    def generate_executive_narrative(self):
        strengths = self.results.get("strengths", [])
        risks = self.results.get("risks", [])

        narrative = "Resumo Executivo Integrado:\n"
        narrative += "Pontos Fortes: " + ", ".join(strengths) + ".\n"
        narrative += "Pontos de Atenção: " + ", ".join(risks) + ".\n"

        return narrative

    def generate_psychodynamic_narrative(self):
        schemas = self.results.get("schemas", [])
        emotional = self.results.get("emotional_analysis", "")
        cognitive = self.results.get("cognitive_analysis", "")

        narrative = "Narrativa Psicodinâmica:\n"
        narrative += f"Esquemas predominantes: {', '.join(schemas)}.\n"
        narrative += f"Dimensão emocional: {emotional}\n"
        narrative += f"Dimensão cognitiva: {cognitive}\n"

        return narrative

    def generate_integrated(self):
        return (
            self.generate_executive_narrative()
            + "\n"
            + self.generate_psychodynamic_narrative()
        )
