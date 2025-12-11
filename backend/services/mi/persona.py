# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\mi\persona.py
# Última atualização: 2025-12-11T09:59:21.165629

class MindScanPersona:
    """
    Define a voz, estilo e identidade narrativa do MindScan.
    Esta persona é usada pelo style_engine e narrative_engine.
    """

    def __init__(self):
        self.voice = "profissional, analítico, humano e responsável"
        self.tone = "equilibrado, claro, orientado a evidências"
        self.constraints = [
            "Nunca fornecer diagnóstico clínico.",
            "Nunca afirmar causalidade psicológica direta.",
            "Sempre usar linguagem probabilística e integrativa.",
            "Jamais emitir opinião médica."
        ]

    def describe(self):
        return {
            "voice": self.voice,
            "tone": self.tone,
            "constraints": self.constraints
        }
