# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\builders\corporate_section_builder.py
# Última atualização: 2025-12-11T09:59:21.120711

# -*- coding: utf-8 -*-
"""
corporate_section_builder.py
----------------------------

Builder auxiliar para montar seções de forma programática,
caso seja necessário expandir seções no futuro.
"""

from typing import Dict, Any, List


class CorporateSectionBuilder:

    def __init__(self):
        self.sections = []

    def add_section(self, section: Dict[str, Any]):
        self.sections.append(section)

    def add(self, id: str, title: str, description: str, blocks: List[Dict[str, str]]):
        self.sections.append({
            "id": id,
            "title": title,
            "description": description,
            "blocks": blocks
        })

    def build(self) -> List[Dict[str, Any]]:
        return self.sections
