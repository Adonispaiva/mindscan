"""
CROSS Big5 × OCAI — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona traços de personalidade (Big Five)
com padrões de cultura organizacional (OCAI):

- Clã (colaborativa)
- Adocracia (inovadora)
- Mercado (competitiva)
- Hierarquia (estruturada)
"""

from typing import Dict, Any


class CrossBig5OCAI:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, big5: Dict[str, float], ocai: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # Abertura × Cultura de inovação
        if big5.get("abertura", 0) >= 65 and ocai.get("inovacao", 0) >= 60:
            patterns["inovador_cultural"] = (
                "Alta abertura alinhada a uma cultura orientada à inovação."
            )

        # Conscienciosidade × Hierarquia
        if big5.get("conscienciosidade", 0) >= 60 and ocai.get("hierarquia", 0) >= 55:
            patterns["excelencia_hierarquica"] = (
                "Perfil altamente disciplinado compatível com cultura estruturada."
            )

        # Amabilidade × Cultura de Clã
        if big5.get("amabilidade", 0) >= 60 and ocai.get("clan", 0) >= 55:
            patterns["ajuste_colaborativo"] = (
                "Alta amabilidade alinhada à cultura colaborativa de Clã."
            )

        # Extroversão × Mercado
        if big5.get("extroversao", 0) >= 60 and ocai.get("mercado", 0) >= 55:
            patterns["agente_competitivo"] = (
                "Extroversão alta alinhada com cultura de mercado e influência social."
            )

        return {
            "module": "cross_big5_ocai",
            "version": self.version,
            "patterns": patterns,
        }
