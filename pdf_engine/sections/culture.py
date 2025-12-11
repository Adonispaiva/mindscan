# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\pdf_engine\sections\culture.py
# Última atualização: 2025-12-11T09:59:27.761619

"""
pdf_engine/sections/culture.py
Seção de Cultura Organizacional do relatório MindScan (OCAI)

Responsabilidades:
- Integrar os resultados do algoritmo OCAI
- Gerar sínteses textuais sobre o perfil cultural atual
- Apresentar a análise de quatro dimensões tradicionais do modelo:
    * Clan
    * Adhocracia
    * Mercado
    * Hierarquia
- Não realiza cálculos — apenas estrutura dados para o PDFBuilder
"""

from typing import Dict, Any


class CultureSection:
    """
    Seção de Cultura Organizacional (OCAI).
    Baseada nos dados normalizados entregues pelo DataLoader.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.ocai = data.get("ocai", {})

    # -------------------------------------------------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------------------------------------------------

    def render(self) -> Dict[str, Any]:
        """
        Retorna a estrutura que será consumida pelo PDFBuilder.
        """
        return {
            "title": "Cultura Organizacional",
            "subtitle": "Análise OCAI — Perfis Culturais",
            "body": self._build_body_text(),
            "scores": self.ocai,
        }

    # -------------------------------------------------------------------------
    # CONSTRUÇÃO DO TEXTO PRINCIPAL
    # -------------------------------------------------------------------------

    def _build_body_text(self) -> str:
        resumo = self._extract_summary()

        return (
            "Esta seção apresenta a leitura do perfil cultural segundo o modelo OCAI, "
            "abrangendo quatro quadrantes principais: Clan, Adhocracia, Mercado e "
            "Hierarquia. A interpretação a seguir resume o posicionamento cultural "
            "identificado a partir dos dados fornecidos.\n\n"
            f"{resumo}"
        )

    # -------------------------------------------------------------------------
    # EXTRAÇÃO DOS DADOS OCAI
    # -------------------------------------------------------------------------

    def _extract_summary(self) -> str:
        if not isinstance(self.ocai, dict):
            return "Os dados de OCAI não estão disponíveis."

        clan = self.ocai.get("clan", "N/D")
        adhocracia = self.ocai.get("adhocracia", "N/D")
        mercado = self.ocai.get("mercado", "N/D")
        hierarquia = self.ocai.get("hierarquia", "N/D")

        return (
            "📗 **OCAI — Clusters Culturais**\n"
            f"- Clan: {clan}\n"
            f"- Adhocracia: {adhocracia}\n"
            f"- Mercado: {mercado}\n"
            f"- Hierarquia: {hierarquia}"
        )


# -------------------------------------------------------------------------
# Função utilitária
# -------------------------------------------------------------------------

def build_culture_section(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interface simples para uso pelo PDFBuilder.
    """
    return CultureSection(data).render()
