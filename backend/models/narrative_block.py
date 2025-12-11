# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\narrative_block.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
narrative_block.py — MindScan ULTRA SUPERIOR
Estrutura de blocos narrativos para relatórios avançados,
incluindo storytelling cognitivo-comportamental e descrições
personalizadas para cada perfil analisado.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class NarrativeBlock:
    title: str
    content: str
    metadata: Dict[str, str]

    def render(self) -> str:
        """Renderiza a narrativa com formatação avançada."""
        return f"{self.title}\n\n{self.content}\n\n— {self.metadata.get('author', 'MindScan')}"
