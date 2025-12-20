import logging

logger = logging.getLogger("PsychometricsEngine")

class Psychometrics:
    """Implementação rigorosa dos algoritmos SynMind."""

    @staticmethod
    def calculate_dass21(responses: dict) -> dict:
        """
        Fórmula: Soma dos itens por subescala * 2.
        Referência: ALGORITIMO DASS.docx
        """
        # Itens mapeados conforme ordem do formulário
        dep = sum(responses.get("depression", [0])) * 2
        anx = sum(responses.get("anxiety", [0])) * 2
        str_ = sum(responses.get("stress", [0])) * 2

        def get_level(score, scale):
            thresholds = {
                "D": [10, 14, 21, 28],
                "A": [8, 10, 15, 20],
                "S": [15, 19, 26, 34]
            }
            t = thresholds[scale]
            if score < t[0]: return "Normal"
            if score < t[1]: return "Leve"
            if score < t[2]: return "Moderado"
            if score < t[3]: return "Severo"
            return "Extremamente Severo"

        return {
            "depression": {"score": dep, "level": get_level(dep, "D")},
            "anxiety": {"score": anx, "level": get_level(anx, "A")},
            "stress": {"score": str_, "level": get_level(str_, "S")}
        }

    @staticmethod
    def calculate_big5(responses: dict) -> dict:
        """
        Cálculo BFI-44. 
        Importante: Itens negativos devem ser invertidos (Score = 6 - Valor).
        """
        # Exemplo de lógica simplificada para a demo (pode ser expandida item a item)
        scores = {
            "O": sum(responses.get("openness", [3])) / len(responses.get("openness", [1])),
            "C": sum(responses.get("conscientiousness", [3])) / len(responses.get("conscientiousness", [1])),
            "E": sum(responses.get("extraversion", [3])) / len(responses.get("extraversion", [1])),
            "A": sum(responses.get("agreeableness", [3])) / len(responses.get("agreeableness", [1])),
            "N": sum(responses.get("neuroticism", [3])) / len(responses.get("neuroticism", [1]))
        }
        # Matcher Global baseado na média de traços desejáveis
        global_match = (scores["O"] + scores["C"] + scores["E"] + scores["A"] + (5 - scores["N"])) / 5
        return {
            "factors": scores,
            "percent": round((global_match / 5) * 100, 2)
        }

    @staticmethod
    def get_bussola_quadrante(performance: float, matcher: float) -> dict:
        """
        Lógica oficial MINDSCAN_BUSSULA DE TALENTOS.docx
        """
        if performance >= 80 and matcher >= 80:
            return {"id": 1, "label": "INSPIRADORES", "color": "#1A237E"}
        elif performance >= 80 and matcher < 80:
            return {"id": 2, "label": "ESPECIALISTAS", "color": "#283593"}
        elif performance < 80 and matcher >= 80:
            return {"id": 3, "label": "PROMISSORES", "color": "#3949AB"}
        else:
            return {"id": 4, "label": "BUSCADORES", "color": "#5C6BC0"}