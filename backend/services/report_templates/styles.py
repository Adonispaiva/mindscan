from reportlab.lib import colors

class SynMindTheme:
    """
    Design System da SynMind para PDFs.
    Baseado no 'Relatório ID RENATA.html' e identidade visual.
    """
    # Paleta de Cores
    PRIMARY_BLUE = colors.HexColor("#1A3A5A")   # Azul Profundo (Logo)
    SECONDARY_GOLD = colors.HexColor("#C5A065") # Dourado/Bege (Detalhes)
    BACKGROUND_CREAM = colors.HexColor("#F8F6F0") # Fundo 'Papel' (Renata)
    TEXT_DARK = colors.HexColor("#2C2C2C")      # Texto Leitura
    TEXT_LIGHT = colors.HexColor("#FFFFFF")
    
    # Fontes (Mapeamento para Standard Type1 do ReportLab por enquanto)
    # Futuramente podemos registrar fontes .ttf externas (Lato, Nixie One)
    FONT_TITLE = "Helvetica-Bold"
    FONT_BODY = "Helvetica"
    FONT_ITALIC = "Helvetica-Oblique"

    @staticmethod
    def get_quadrant_color(quadrante: str):
        mapping = {
            "ESPECIALISTAS": "#2E86AB",
            "RELACIONAIS": "#D90429",
            "ANALÍTICOS": "#8D99AE",
            "INOVADORES": "#EF233C"
        }
        return colors.HexColor(mapping.get(quadrante.upper(), "#1A3A5A"))