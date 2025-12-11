# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\instrument_normalizer.py
# Última atualização: 2025-12-11T09:59:20.761538

class InstrumentNormalizer:
    """
    Esta camada permite padronizar inputs específicos
    de instrumentos como Big5, TEIQue, OCAI, DASS21, etc.
    Sem alterar o motor científico.
    """

    @staticmethod
    def normalize_instrument(name: str, data: dict) -> dict:

        normalized = {}

        for key, value in data.items():
            # Exemplo: remover prefixos indesejados
            clean_key = key.replace(f"{name}_", "")
            normalized[clean_key] = value

        return normalized
