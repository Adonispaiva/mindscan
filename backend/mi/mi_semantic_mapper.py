# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_semantic_mapper.py
# Última atualização: 2025-12-11T09:59:20.872348

class MISemanticMapper:
    """
    Constrói mapas semânticos que relacionam traços,
    competências, estilos e narrativas.
    """

    @staticmethod
    def build_map(results: dict) -> dict:
        if not results:
            return {}

        semantic_map = {}

        # Relação Big5 → Competências
        if "big5" in results:
            big5 = results["big5"]
            semantic_map["competency_alignment"] = {
                "liderança": big5.get("extroversao", 0) + big5.get("abertura", 0),
                "estabilidade": big5.get("neuroticismo", 100) * -1,
                "colaboração": big5.get("amabilidade", 0),
            }

        # Relação TEIQue → Adaptabilidade
        if "teique" in results:
            tei = results["teique"]
            semantic_map["emotional_alignment"] = {
                "autogestao": tei.get("autocontrole", 0),
                "percepção_social": tei.get("empatia", 0),
            }

        return semantic_map
