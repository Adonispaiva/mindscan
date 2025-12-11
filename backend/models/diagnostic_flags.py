# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\diagnostic_flags.py
# Última atualização: 2025-12-11T09:59:20.948776

"""
diagnostic_flags.py — MindScan ULTRA SUPERIOR
Marcações de diagnóstico utilizadas por diversas engines.
Permitem detecção precoce de riscos, padrões anômalos e conflitos cognitivos.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DiagnosticFlags:
    """Conjunto de marcadores diagnósticos MindScan."""
    flags: Dict[str, Any]

    def add_flag(self, name: str, value: Any):
        """Adiciona um novo marcador."""
        self.flags[name] = value

    def has_risk(self) -> bool:
        """Retorna True se houver algum risco detectado."""
        for v in self.flags.values():
            if isinstance(v, bool) and v:
                return True
            if isinstance(v, (int, float)) and v > 0:
                return True
        return False
