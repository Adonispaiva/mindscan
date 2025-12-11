# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\design\corporate_icon_loader.py
# Última atualização: 2025-12-11T09:59:21.143695

# -*- coding: utf-8 -*-
"""
corporate_icon_loader.py
------------------------

Carrega ícones corporativos usados no HTML/PDF.
Esses ícones podem ser SVG inline ou caminhos externos.
"""

from typing import Dict


class CorporateIconLoader:

    ICONS = {
        "check": "<svg width='14' height='14' fill='#0066CC'><path d='M5.6 10.2L2.4 7l1.2-1.2 2 2 5-5 1.2 1.2z' /></svg>",
        "alert": "<svg width='14' height='14' fill='#CC3300'><path d='M7 1l6 12H1L7 1zm0 3l-.7 4.5h1.4L7 4zm0 6v1.5h.01H7z' /></svg>",
        "arrow_right": "<svg width='14' height='14' fill='#4D4F52'><path d='M5 3l4 4-4 4V3z' /></svg>",
    }

    @classmethod
    def get(cls, name: str) -> str:
        return cls.ICONS.get(name, "")

    @classmethod
    def all(cls) -> Dict[str, str]:
        return cls.ICONS.copy()
