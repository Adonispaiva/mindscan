# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_output_formatter.py
# Última atualização: 2025-12-11T09:59:20.620871

from __future__ import annotations
from typing import Dict, Any


class BussolaOutputFormatter:
    """
    Formata os resultados da Bússola para uso em:
        - relatórios
        - insights
        - dashboards
    """

    def format(self, data: Dict[str, Any]) -> Dict[str, Any]:

        coords = data.get("coordinates", {})
        dirs = data.get("directions", {})
        metrics = data.get("metrics", {})

        return {
            "coordenadas": coords,
            "direcao": dirs,
            "metricas": metrics,
            "descricao": self._gerar_descricao(dirs)
        }

    def _gerar_descricao(self, dirs: Dict[str, Any]) -> str:

        quad = dirs.get("quadrant", "Indefinido")
        angle = dirs.get("angle", 0)

        return f"A direção predominante é '{quad}', com ângulo comportamental de {angle:.1f}°."
