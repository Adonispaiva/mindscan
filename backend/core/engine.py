from typing import Dict, Any
from backend.core.normalizer import Normalizer
from backend.core.nlp_processor import NLPProcessor
from backend.core.scoring import ScoringEngine
from backend.core.diagnostic_engine import DiagnosticEngine
from backend.services.runtime_interface import RuntimeInterface


class MindScanEngine:
    """
    Núcleo superior do MindScan 2.0.

    Orquestra:
    - normalização dos dados psicométricos
    - processamento NLP
    - agregação dos instrumentos
    - cálculo dos scores
    - geração do diagnóstico consolidado
    """

    def __init__(self):
        self.normalizer = Normalizer()
        self.nlp = NLPProcessor()
        self.scoring = ScoringEngine()
        self.diagnostic = DiagnosticEngine()

    # ------------------------------------------------------------
    #  Pipeline completo do MindScan
    # ------------------------------------------------------------
    def process(self, dataset: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Validação mínima
        if not RuntimeInterface.validate_input(dataset):
            raise ValueError("Dataset inválido para a MindScanEngine.")

        # 2. Normalização
        normalized = self.normalizer.normalize(dataset)

        # 3. NLP (texto adicional, notas, feedbacks etc.)
        nlp_processed = self.nlp.process(normalized)

        # 4. Scoring psicométrico dos instrumentos
        scores = self.scoring.compute_scores(nlp_processed)

        # 5. Diagnóstico final consolidado
        diagnosis = self.diagnostic.generate_diagnosis(scores)

        # 6. Preparar o resultado padrão MindScan
        output = RuntimeInterface.format_engine_output(diagnosis)
        output["scores"] = scores
        output["insights"] = diagnosis.get("insights")
        output["profile"] = diagnosis.get("profile")

        return output
