# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_adaptive_personality_shift.py
# Última atualização: 2025-12-11T09:59:20.887954

class MIAdaptivePersonalityShift:
    """
    Prediz mudanças de personalidade a médio prazo (6–12 meses).
    """

    @staticmethod
    def shift(results: dict) -> dict:
        big5 = results.get("big5", {})
        shift_map = {}

        for trait, val in big5.items():
            direction = 1 if val < 55 else -1
            shift_map[trait] = round(val + direction * 2.5, 2)

        return shift_map
