# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\core\normalization\global_normalization.py
# Última atualização: 2025-12-11T09:59:20.792728

class GlobalNormalization:
    """
    Aplica normalização final a todos os blocos do MindScan
    para manter coerência entre instrumentos.
    """

    @staticmethod
    def normalize_block(block: dict) -> dict:
        if not isinstance(block, dict):
            return block
        max_val = max(block.values()) if block else 1
        return {k: round((v / max_val) * 100, 2) for k, v in block.items()}

    @staticmethod
    def apply(results: dict) -> dict:
        normalized = {}
        for key, block in results.items():
            if isinstance(block, dict):
                normalized[key] = GlobalNormalization.normalize_block(block)
            else:
                normalized[key] = block
        return normalized
