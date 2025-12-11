# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\core\psyc_core_service.py
# Última atualização: 2025-12-11T09:59:21.138689

# D:\mindscan\backend\services\core\psych_core_service.py
# --------------------------------------------------------
# Serviço psicodinâmico central do MindScan — SynMind
# Autor: Leo Vinci — Inovexa Software
#
# Fornece leitura integrada de:
# - Esquemas (Young)
# - TEIQue
# - Big Five
# - DASS21
# - Cruzamentos estruturais MindScan
#
# É utilizado por:
# - Narrativa psicodinâmica (renderer)
# - Resumo executivo
# - Sinalização de riscos e forças emocionais
# - Motor premium

from typing import Any, Dict, List

from .base_service import BaseService
from .data_service import DataService

from backend.backend.algorithms.esquemas.esquemas_summary import EsquemasSummary
from backend.backend.algorithms.big5.big5_summary import Big5Summary
from backend.backend.algorithms.teique.teique_summary import TeiqueSummary
from backend.backend.algorithms.dass21.dass21_summary import Dass21Summary
from backend.backend.algorithms.cruzamentos.cross_engine import CrossEngine


class PsychCoreService(BaseService):
    """
    Serviço psicodinâmico central.
    Concentra interpretações profundas e relações emocionais,
    cognitivas, comportamentais e de risco.
    """

    def __init__(self):
        super().__init__("PsychCoreService")
        self.data_service = DataService()
        self.esquemas = EsquemasSummary()
        self.big5 = Big5Summary()
        self.teique = TeiqueSummary()
        self.dass = Dass21Summary()
        self.cross = CrossEngine()

    # ----------------------------------------------------------------------
    # INTERPRETAÇÕES NUCLEARES
    # ----------------------------------------------------------------------

    def _interpret_esquemas(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retorna leituras psicodinâmicas derivadas do modelo de Young.
        """
        return self.esquemas.build_summary(scores.get("esquemas", {}))

    def _interpret_big5(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpretação de personalidade.
        """
        return self.big5.build_summary(scores.get("big5", {}))

    def _interpret_teique(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inteligência emocional + padrões de regulação emocional.
        """
        return self.teique.build_summary(scores.get("teique", {}))

    def _interpret_dass(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estresse, ansiedade, depressão — visão clínica leve contextualizada.
        """
        return self.dass.build_summary(scores.get("dass21", {}))

    # ----------------------------------------------------------------------
    # CRUZAMENTOS PSICODINÂMICOS
    # ----------------------------------------------------------------------

    def _cross_psychodynamics(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ligações entre personalidade, emoção, esquemas, cultura e riscos.
        """
        return self.cross.run_cross_analysis(scores)

    # ----------------------------------------------------------------------
    # PIPELINE PRINCIPAL
    # ----------------------------------------------------------------------

    def build_psychodynamic_profile(self, test_id: str) -> Dict[str, Any]:
        """
        Gera o perfil psicodinâmico completo.
        """
        self._log(f"Gerando perfil psicodinâmico para test_id={test_id}")

        data = self.data_service.get_report_ready_data(test_id)
        scores = data["scores"]

        return {
            "esquemas": self._interpret_esquemas(scores),
            "big5": self._interpret_big5(scores),
            "teique": self._interpret_teique(scores),
            "dass": self._interpret_dass(scores),
            "crosslinks": self._cross_psychodynamics(scores),
            "meta": {
                "test_id": data["test_id"],
                "timestamp": data["timestamp"],
            },
        }

    # ----------------------------------------------------------------------
    # MÉTODO PADRÃO DE EXECUÇÃO
    # ----------------------------------------------------------------------

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execução genérica prevista pela BaseService.
        """
        self._log("Executando pacote psicodinâmico.")
        self._validate_input(data)
        packaged = self._package_metadata(data)
        return packaged
