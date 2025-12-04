"""
pdf_engine/sections/final_report.py
Seção final do relatório MindScan

Responsabilidades:
- Apresentar conclusão geral do diagnóstico
- Integrar recomendações baseadas nos resultados (sem cálculos)
- Gerar texto de fechamento do relatório
- Retornar estrutura consumível pelo PDFBuilder
"""

from typing import Dict, Any


class FinalReportSection:
    """
    Seção de conclusão e recomendações do MindScan.
    Baseada nos dados normalizados entregues pelo DataLoader.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data

        # Acesso direto às principais estruturas consolidadas:
        self.big5 = data.get("big5", {})
        self.teique = data.get("teique", {})
        self.dass21 = data.get("dass21", {})
        self.esquemas = data.get("esquemas", {})
        self.performance = data.get("performance", {})
        self.ocai = data.get("ocai", {})
        self.bussola = data.get("bussola", {})
        self.cruz = data.get("cruzamentos", {})

    # -------------------------------------------------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------------------------------------------------

    def render(self) -> Dict[str, Any]:
        """
        Retorna estrutura consumida pelo PDFBuilder.
        Inclui:
        - título
        - texto de fechamento
        - recomendações
        """
        return {
            "title": "Conclusão Geral",
            "subtitle": "Síntese Integrada do Perfil MindScan",
            "body": self._build_body_text(),
            "recommendations": self._build_recommendations(),
        }

    # -------------------------------------------------------------------------
    # TEXTO PRINCIPAL
    # -------------------------------------------------------------------------

    def _build_body_text(self) -> str:
        return (
            "Esta seção apresenta a conclusão geral do MindScan, consolidando os "
            "principais aspectos do perfil psicológico, emocional, comportamental e "
            "organizacional do participante. Os dados integrados fornecem uma visão "
            "abrangente, equilibrada e precisa do funcionamento pessoal e profissional."
        )

    # -------------------------------------------------------------------------
    # RECOMENDAÇÕES
    # -------------------------------------------------------------------------

    def _build_recommendations(self) -> Dict[str, Any]:
        """
        Gera recomendações gerais com base nos blocos disponíveis.
        Não executa cálculos — apenas dá estrutura textual organizada.
        """

        recs = []

        # Exemplos baseados em padrões gerais:
        if isinstance(self.teique, dict):
            recs.append("Desenvolver competências de inteligência emocional para aumentar a adaptação e o equilíbrio psicológico.")

        if isinstance(self.performance, dict):
            recs.append("Manter práticas que favoreçam produtividade constante e monitorar evolução de entregas.")

        if isinstance(self.dass21, dict):
            recs.append("Observar indicadores emocionais (ansiedade, depressão e estresse) para prevenir sobrecargas futuras.")

        if isinstance(self.big5, dict):
            recs.append("Aproveitar traços fortes de personalidade como alavancas para crescimento profissional.")

        if isinstance(self.ocai, dict):
            recs.append("Alinhar o perfil individual com o ambiente organizacional para maximizar engajamento e bem-estar.")

        if isinstance(self.esquemas, dict):
            recs.append("Identificar padrões cognitivos recorrentes para promover autodesenvolvimento e resiliência.")

        return {
            "summary": "Recomendações gerais baseadas no conjunto integrado de resultados:",
            "items": recs or ["Nenhuma recomendação disponível."],
        }


# -------------------------------------------------------------------------
# Função utilitária
# -------------------------------------------------------------------------

def build_final_report_section(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interface simples para uso pelo PDFBuilder.
    """
    return FinalReportSection(data).render()
