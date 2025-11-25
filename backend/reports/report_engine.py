# ============================================================
# MindScan — Report Engine
# ============================================================
# O Report Engine é responsável por transformar o MI Package
# e todos os blocos psicométricos em um relatório estruturado,
# pronto para exportação e renderização (PDF, HTML ou API).
#
# Funções:
# - Estruturar o relatório MindScan
# - Incorporar quadrante final
# - Inserir blocos de texto MI já formatados
# - Gerar narrativa final
#
# Versão: 2.0 — Arquitetura SynMind 2025
# ============================================================

from typing import Dict, Any
from backend.mi.mi_formatter import MIFormatter


class ReportEngine:
    """
    Responsável pela montagem completa do relatório MindScan.
    """

    def __init__(self):
        self.formatter = MIFormatter()

    # ------------------------------------------------------------
    # BLOCO — CABEÇALHO
    # ------------------------------------------------------------
    def header_block(self, subject_name: str) -> str:
        return (
            f"RELATÓRIO MINDSCAN\n"
            f"Sujeito avaliado: {subject_name}\n"
            f"Versão do Sistema: v2.0\n"
            f"-------------------------------------------\n"
        )

    # ------------------------------------------------------------
    # BLOCO — QUADRANTE FINAL
    # ------------------------------------------------------------
    def quadrant_block(self, mi_package: Dict[str, Any]) -> str:
        return (
            "QUADRANTE FINAL (Bússola MindScan)\n"
            f"Quadrante: {mi_package['quadrant']}\n"
            f"Coordenadas: X = {mi_package['coordinates']['x']} | "
            f"Y = {mi_package['coordinates']['y']}\n"
            f"Estilo: {mi_package['style']}\n"
            f"Nível de Risco: {mi_package['risk_level']}\n"
            "-------------------------------------------\n"
        )

    # ------------------------------------------------------------
    # BLOCO — TALENTOS
    # ------------------------------------------------------------
    def talents_block(self, mi_package: Dict[str, Any]) -> str:
        return self.formatter.format_talents(mi_package["talents"]) + "\n" \
            + "-------------------------------------------\n"

    # ------------------------------------------------------------
    # BLOCO — RISCOS
    # ------------------------------------------------------------
    def risks_block(self, mi_package: Dict[str, Any]) -> str:
        return self.formatter.format_risks(mi_package["risks"]) + "\n" \
            + "-------------------------------------------\n"

    # ------------------------------------------------------------
    # BLOCO — CONTRADIÇÕES
    # ------------------------------------------------------------
    def contradictions_block(self, mi_package: Dict[str, Any]) -> str:
        return self.formatter.format_contradictions(mi_package["contradictions"]) + "\n" \
            + "-------------------------------------------\n"

    # ------------------------------------------------------------
    # BLOCO — RECOMENDAÇÕES
    # ------------------------------------------------------------
    def recommendations_block(self, mi_package: Dict[str, Any]) -> str:
        return self.formatter.format_recommendations(mi_package["recommendations"]) + "\n" \
            + "-------------------------------------------\n"

    # ------------------------------------------------------------
    # RELATÓRIO COMPLETO
    # ------------------------------------------------------------
    def build_report(
        self,
        subject_name: str,
        mi_package: Dict[str, Any]
    ) -> str:
        """
        Gera o relatório completo em formato textual.
        Pode ser exportado para PDF, HTML ou API.
        """

        parts = [
            self.header_block(subject_name),
            self.quadrant_block(mi_package),
            self.talents_block(mi_package),
            self.risks_block(mi_package),
            self.contradictions_block(mi_package),
            self.recommendations_block(mi_package)
        ]

        return "\n".join(parts)


# Instância pública
report_engine = ReportEngine()
