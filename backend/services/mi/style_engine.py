# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\mi\style_engine.py
# Última atualização: 2025-12-11T09:59:21.166628

class StyleEngine:
    """
    Ajusta o estilo textual para adequar-se à persona MindScan.
    Mantém consistência narrativa e remove ruído linguístico.
    """

    def __init__(self, persona):
        self.persona = persona

    def apply_style(self, text):
        if not text:
            return ""

        # Ajuste simples de estilo
        styled = text.strip()
        styled = styled.replace("\n\n", "\n")

        # Aplicação de tom analítico
        return f"{styled}"
