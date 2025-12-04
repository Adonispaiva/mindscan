"""
OCAI Output Formatter
Formata a saída do OCAI para o padrão MindScanEngine.
"""

from typing import Dict, Any


class OCAIOutputFormatter:
    """
    Gera o payload final que será consumido pelos módulos
    de profile engines e pelos renderizadores de relatório.
    """

    def __init__(self):
        self.version = "1.0"

    def format(self,
               dims: Dict[str, float],
               descriptives: Dict[str, str],
               crosslinks: Dict[str, Any],
               alerts: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "module": "OCAI",
            "version": self.version,
            "dimensions": dims,
            "descriptives": descriptives,
            "crosslinks": crosslinks,
            "alerts": alerts,
        }
