# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\cruzamentos\cross_big5_performance.py
# Última atualização: 2025-12-11T09:59:20.636480

"""
CROSS Big5 × Performance — Versão ULTRA SUPERIOR
-------------------------------------------------------------

Relaciona traços de personalidade (Big Five) com indicadores
de performance comportamental e operacional.

Exemplos de eixos avaliados:
- produtividade
- foco
- consistência
- adaptabilidade
- execução prática
"""

from typing import Dict, Any


class CrossBig5Performance:
    def __init__(self):
        self.version = "2.0-ultra"

    def generate(self, big5: Dict[str, float], perf: Dict[str, float]) -> Dict[str, Any]:
        patterns = {}

        # Conscienciosidade → Consistência
        if big5.get("conscienciosidade", 0) >= 65:
            if perf.get("consistencia", 0) >= 50:
                patterns["execucao_forte"] = (
                    "Alta conscienciosidade alinhada à consistência operacional."
                )
            else:
                patterns["potencial_nao_aplicado"] = (
                    "Conscienciosidade alta, mas a consistência prática não acompanha."
                )

        # Abertura → Adaptabilidade
        if big5.get("abertura", 0) >= 70 and perf.get("adaptabilidade", 0) >= 50:
            patterns["inovacao_adaptativa"] = (
                "Abertura elevada amplificando capacidade de adaptação inovadora."
            )

        # Extroversão × Comunicação
        if big5.get("extroversao", 0) >= 60:
            if perf.get("comunicacao", 0) < 40:
                patterns["extroversao_ineficiente"] = (
                    "Extroversão alta sem comunicação eficaz — desalinhamento crítico."
                )
            else:
                patterns["comunicador_natural"] = (
                    "Extroversão alta bem utilizada para comunicação e influência."
                )

        # Amabilidade × Trabalho em equipe
        if big5.get("amabilidade", 0) >= 55 and perf.get("colaboracao", 0) >= 50:
            patterns["colaborador_estrategico"] = (
                "Amabilidade forte resultando em alto desempenho colaborativo."
            )

        return {
            "module": "cross_big5_performance",
            "version": self.version,
            "patterns": patterns,
        }
