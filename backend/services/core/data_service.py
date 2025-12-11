# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\core\data_service.py
# Última atualização: 2025-12-11T09:59:21.120711

# D:\mindscan\backend\services\core\data_service.py
# --------------------------------------------------
# Serviço central de dados do MindScan — SynMind
# Autor: Leo Vinci — Inovexa Software
# Arquivo definitivo, integrado e alinhado ao ecossistema MindScan.

from typing import Any, Dict, Optional
from datetime import datetime

from backend.database import Database
from backend.core.runtime_kernel import RuntimeKernel
from backend.core.normalizer import Normalizer
from backend.core.scoring import ScoringEngine
from backend.core.diagnostic_engine import DiagnosticEngine


class DataService:
    """
    Serviço corporativo responsável por:
    - carregar payloads de psicometria
    - normalizar dados brutos
    - integrar resultados com o pipeline do MindScan
    - consolidar metadados, timestamps e trilhas técnicas
    - fornecer entrada limpa para renderizadores PDF
    """

    def __init__(self):
        self.db = Database()
        self.kernel = RuntimeKernel()
        self.normalizer = Normalizer()
        self.scoring = ScoringEngine()
        self.diagnostic = DiagnosticEngine()

    # --------------------------------------------------------------
    # UTILIDADES CENTRAIS
    # --------------------------------------------------------------

    def load_raw_payload(self, test_id: str) -> Dict[str, Any]:
        """
        Recupera os dados brutos associados ao test_id.
        """
        record = self.db.get_test_payload(test_id)
        if not record:
            raise ValueError(f"Payload não encontrado para test_id: {test_id}")

        return record

    def normalize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica normalização completa sobre variáveis psicométricas,
        estruturas, metadados e vetores brutos.
        """
        normalized = self.normalizer.normalize(payload)
        return normalized

    def compute_scores(self, normalized: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a pontuação final de todos os módulos:
        BIG5, TEIQue, Esquemas, DASS, OCAI, Performance,
        e integra com o motor de cruzamentos.
        """
        scores = self.scoring.compute_scores(normalized)
        return scores

    def run_diagnostic(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Chama o motor de diagnóstico técnico/narrativo.
        """
        diagnostics = self.diagnostic.run(scores)
        return diagnostics

    # --------------------------------------------------------------
    # PIPELINE COMPLETO
    # --------------------------------------------------------------

    def assemble_results(self, test_id: str) -> Dict[str, Any]:
        """
        Pipeline consolidado que gera o “pacote final de dados”
        para os renderizadores PDF.
        """
        raw_payload = self.load_raw_payload(test_id)
        normalized = self.normalize_payload(raw_payload)
        scores = self.compute_scores(normalized)
        diagnostics = self.run_diagnostic(scores)

        return {
            "test_id": test_id,
            "timestamp": datetime.utcnow().isoformat(),
            "raw_payload": raw_payload,
            "normalized": normalized,
            "scores": scores,
            "diagnostics": diagnostics,
            "kernel_runtime": self.kernel.get_runtime_metadata(),
        }

    # --------------------------------------------------------------
    # INTERFACE EXTERNA PARA REPORTSERVICE
    # --------------------------------------------------------------

    def get_report_ready_data(self, test_id: str) -> Dict[str, Any]:
        """
        Retorna o “pacote final” pronto para renderização
        pelos templates corporativos do MindScan.
        """
        return self.assemble_results(test_id)
