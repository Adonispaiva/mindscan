# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\core\scale_normalizer.py
# Última atualização: 2025-12-11T09:59:20.620871

class ScaleNormalizer:
    """
    Normaliza escalas de diferentes instrumentos para níveis comparáveis.
    Exemplo: converter escalas 1–5, 1–7, 0–3 para uma escala comum 0–100.
    """

    @staticmethod
    def normalize(value: float, min_val: float, max_val: float) -> float:
        if max_val == min_val:
            return 0
        return round(((value - min_val) / (max_val - min_val)) * 100, 2)

    @staticmethod
    def batch_normalize(data: dict, min_val: float, max_val: float) -> dict:
        return {k: ScaleNormalizer.normalize(v, min_val, max_val) for k, v in data.items()}
