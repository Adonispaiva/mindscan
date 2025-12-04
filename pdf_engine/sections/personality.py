"""
pdf_engine/sections/personality.py
Seção de Personalidade — Big Five (OCEAN)

Responsabilidades:
- Integrar resultados do Big Five consolidados
- Apresentar fatores OCEAN: Abertura, Conscienciosidade, Extroversão,
  Amabilidade e Estabilidade Emocional
- Organizar a estrutura textual + pontuações para o PDFBuilder

Não executa cálculos — apenas apresenta os dados já gerados pelos algoritmos.
"""

from typing import Dict, Any


class PersonalitySection:
    """
    Seção de Personalidade (Big Five).
    Recebe os dados normalizados pelo DataLoader.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.big5 = data.get("big5", {})

    # -------------------------------------------------------------------------
    # MÉTODO PRINCIPAL
    # -------------------------------------------------------------------------

    def render(self) -> Dict[str, Any]:
        """
        Retorna uma estrutura formatada para o PDFBuilder.
        """
        return {
            "title": "Perfil de Personalidade",
            "subtitle": "Modelo Big Five (OCEAN)",
            "body": self._build_body_text(),
            "scores": self.big5,
        }

    # -------------------------------------------------------------------------
    # TEXTO PRINCIPAL
    # -------------------------------------------------------------------------

    def _build_body_text(self) -> str:
        resumo = self._extract_summary()

        return (
            "A seguir, apresentamos o perfil de personalidade baseado no modelo Big Five "
            "(OCEAN). Esta abordagem avalia cinco dimensões fundamentais que descrevem "
            "o comportamento humano de forma estável e consistente.\n\n"
            f"{resumo}"
        )

    # -------------------------------------------------------------------------
    # RESUMO DO BIG FIVE
    # -------------------------------------------------------------------------

    def _extract_summary(self) -> str:
        if not isinstance(self.big5, dict):
            return "Os dados de personalidade não estão disponíveis."

        abertura = self.big5.get("abertura", "N/D")
        consc = self.big5.get("consciencia", "N/D")
        ext = self.big5.get("extroversao", "N/D")
        amabilidade = self.big5.get("amabilidade", "N/D")
        neuro = self.big5.get("neuroticismo", "N/D")

        return (
            "📗 **Big Five — Dimensões Avaliadas:**\n"
            f"- Abertura: {abertura}\n"
            f"- Conscienciosidade: {consc}\n"
            f"- Extroversão: {ext}\n"
            f"- Amabilidade: {amabilidade}\n"
            f"- Estabilidade Emocional (Neuroticismo inverso): {neuro}"
        )


# -------------------------------------------------------------------------
# Função utilitária
# -------------------------------------------------------------------------

def build_personality_section(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interface simples para uso pelo PDFBuilder.
    """
    return PersonalitySection(data).render()
