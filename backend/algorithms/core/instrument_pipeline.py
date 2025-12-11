# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\core\instrument_pipeline.py
# Última atualização: 2025-12-11T09:59:20.620871

class InstrumentPipeline:
    """
    Executa a sequência de etapas de um instrumento:
    - normalização
    - verificação estatística
    - interpretação
    - score final
    """

    def __init__(self, normalizer, verifier, interpreter):
        self.normalizer = normalizer
        self.verifier = verifier
        self.interpreter = interpreter

    def run(self, raw_data: dict) -> dict:
        normalized = self.normalizer(raw_data)
        anomalies = self.verifier(normalized)
        interpreted = self.interpreter(normalized)

        return {
            "normalized": normalized,
            "anomalies": anomalies,
            "interpreted": interpreted
        }
