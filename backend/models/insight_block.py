# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\insight_block.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
insight_block.py — MindScan ULTRA SUPERIOR
Bloco modular de insights, contendo unidades de percepção analítica
geradas por motores cognitivos e algoritmos de profundidade emocional,
comportamental e estratégica.

Utilizado em:
- Summaries
- Relatórios PDF
- Engines de Insight
- Pipelines avançados
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class InsightBlock:
    """Estrutura mínima de um insight isolado."""
    title: str
    description: str
    intensity: float
    metadata: Dict[str, Any]

    def formatted(self) -> Dict[str, Any]:
        """Retorna o insight formatado para exibição ou relatório."""
        return {
            "title": self.title,
            "description": self.description,
            "intensity": max(0.0, min(100.0, self.intensity)),
            "metadata": self.metadata,
        }


@dataclass
class InsightBundle:
    """Coleção estruturada de insights."""
    insights: List[InsightBlock]

    def summarize_intensity(self) -> float:
        """Calcula intensidade média dos insights."""
        if not self.insights:
            return 0.0
        total = sum(i.intensity for i in self.insights)
        return total / len(self.insights)
