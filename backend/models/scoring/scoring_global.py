# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_global.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringGlobal(BaseModel):
    """
    Estrutura global agregada de scoring do MindScan.

    Aqui convergem:
    - pesos integrados,
    - índices gerais,
    - normalizações,
    - fatores compostos.

    É consumida pela MI e pelo pipeline de relatório.
    """

    global_factors: Dict[str, float] = Field(default_factory=dict)
    composite_index: Dict[str, float] = Field(default_factory=dict)
    module_weights: Dict[str, float] = Field(default_factory=dict)

    metadata: Dict[str, Any] = Field(default_factory=dict)
