# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_development_path_generator.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIDevelopmentPathGenerator:
    """
    Cria caminhos de desenvolvimento personalizados
    baseados no conjunto completo de resultados.
    """

    @staticmethod
    def generate(results: dict) -> dict:
        path = []

        if results.get("performance_estimate", 50) < 60:
            path.append("Fortalecer disciplina operacional e planejamento semanal.")

        if "risks" in results and results["risks"]:
            path.append("Aprimorar estratégias de autogestão emocional.")

        if results.get("global_score", 50) > 70:
            path.append("Assumir desafios estratégicos e mentoria de equipes.")

        return {
            "development_steps": path,
            "steps_count": len(path)
        }
