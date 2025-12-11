# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_narrative_polisher.py
# Última atualização: 2025-12-11T09:59:20.856706

class MINarrativePolisher:
    """
    Refina textos brutos gerados pela MI,
    garantindo fluidez, coerência e voz institucional.
    """

    @staticmethod
    def polish(text: str) -> str:
        if not text:
            return ""

        # Ajustes simples — a versão Enterprise usa modelos externos
        text = text.strip()
        text = text.replace("  ", " ")
        if not text.endswith("."):
            text += "."

        # Regras institucionais básicas
        replacements = {
            "não adequado": "não recomendado",
            "ruim": "desfavorável",
            "fraco": "pouco desenvolvido",
        }

        for src, tgt in replacements.items():
            text = text.replace(src, tgt)

        return text
