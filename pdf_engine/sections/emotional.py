# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\pdf_engine\sections\emotional.py
# Última atualização: 2025-12-11T09:59:27.761619

"""
pdf_engine/sections/emotional.py
Seção emocional do relatório MindScan

Responsabilidades:
- Integrar resultados de TEIQue (Inteligência Emocional)
- Integrar resultados de DASS-21 (Ansiedade, Depressão, Estresse)
- Preparar texto e blocos estruturados para o PDFBuilder
- Não executar cálculos psicométricos (já feitos no core dos algoritmos)
"""

from typing import Dict, Any


class EmotionalSection:
    """
    Seção emocional do MindScan.
    Baseada nos dados normalizados entregues pelo DataLoader.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.teique = data.get("teique", {})
        self.dass21 = data.get("dass21", {})

    # -------------------------------------------------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------------------------------------------------

    def render(self) -> Dict[str, Any]:
        """
        Retorna a estrutura que será consumida pelo PDFBuilder.
        """
        return {
            "title": "Seção Emocional",
            "subtitle": "Inteligência Emocional (TEIQue) e Saúde Emocional (DASS-21)",
            "body": self._build_body_text(),
            "scores": {
                "teique": self.teique,
                "dass21": self.dass21,
            },
        }

    # -------------------------------------------------------------------------
    # CONSTRUÇÃO DO TEXTO
    # -------------------------------------------------------------------------

    def _build_body_text(self) -> str:
        teique_sumario = self._extract_teique_summary()
        dass_sumario = self._extract_dass_summary()

        return (
            "Esta seção apresenta uma visão integrada sobre a saúde emocional do "
            "participante, combinando Inteligência Emocional (TEIQue) e indicadores "
            "de estresse, ansiedade e depressão (DASS-21).\n\n"
            f"{teique_sumario}\n\n"
            f"{dass_sumario}"
        )

    # -------------------------------------------------------------------------
    # TEIQue
    # -------------------------------------------------------------------------

    def _extract_teique_summary(self) -> str:
        """
        Gera um resumo textual do TEIQue baseado nos dados disponíveis.
        """

        if not isinstance(self.teique, dict):
            return "Os dados de TEIQue não estão disponíveis."

        # Campos comuns em TEIQue — adaptáveis
        fatores = []
        for chave, valor in self.teique.items():
            if isinstance(valor, (int, float)):
                fatores.append(f"- {chave.capitalize()}: {valor}")

        fatores_txt = "\n".join(fatores)

        return (
            "📘 **TEIQue — Inteligência Emocional**\n"
            "O TEIQue avalia fatores como autocontrole, sociabilidade, bem-estar e "
            "gestão emocional.\n\n"
            f"{fatores_txt if fatores_txt else 'Nenhum dado detalhado disponível.'}"
        )

    # -------------------------------------------------------------------------
    # DASS-21
    # -------------------------------------------------------------------------

    def _extract_dass_summary(self) -> str:
        """
        Gera um resumo textual da DASS-21.
        """

        if not isinstance(self.dass21, dict):
            return "Os dados do DASS-21 não estão disponíveis."

        ansiedade = self.dass21.get("ansiedade", "N/D")
        depressao = self.dass21.get("depressao", "N/D")
        estresse = self.dass21.get("estresse", "N/D")

        return (
            "📙 **DASS-21 — Saúde Emocional**\n"
            "A DASS-21 avalia níveis de ansiedade, depressão e estresse.\n\n"
            f"- Ansiedade: {ansiedade}\n"
            f"- Depressão: {depressao}\n"
            f"- Estresse: {estresse}"
        )


# -------------------------------------------------------------------------
# Função utilitária
# -------------------------------------------------------------------------

def build_emotional_section(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interface direta para uso pelo PDFBuilder.
    """
    return EmotionalSection(data).render()
