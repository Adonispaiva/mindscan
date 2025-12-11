# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\mi\compliance_filter.py
# Última atualização: 2025-12-11T09:59:21.161636

import re

class ComplianceFilter:
    """
    Remove expressões ilegais ou proibidas:
    - Diagnósticos clínicos
    - Termos psiquiátricos diretos
    - Afirmações absolutas sobre saúde mental
    """

    PROHIBITED_PATTERNS = [
        r"depressão clínica",
        r"transtorno",
        r"diagnóstico",
        r"esquizofrenia",
        r"bipolar",
        r"TAG",
        r"TDAH"
    ]

    def filter(self, text):
        if not text:
            return ""

        sanitized = text

        for pattern in self.PROHIBITED_PATTERNS:
            sanitized = re.sub(pattern, "[informação suprimida]", sanitized, flags=re.IGNORECASE)

        # Remove afirmações absolutas
        sanitized = re.sub(r"sempre|nunca|garante|certeza", "[termo moderado]", sanitized, flags=re.IGNORECASE)

        return sanitized
