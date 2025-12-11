# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\helpers\html_sanitizer.py
# Última atualização: 2025-12-11T09:59:21.153629

# -*- coding: utf-8 -*-
"""
html_sanitizer.py
-----------------

Sanitizador de HTML antes da renderização.
Remove trechos inválidos, tags obsoletas, espaços redundantes
e garante compatibilidade com o motor de PDF.
"""

import re
from typing import Dict


class HTMLSanitizer:

    @staticmethod
    def remove_empty_tags(html: str) -> str:
        html = re.sub(r"<p>\s*</p>", "", html)
        html = re.sub(r"<div>\s*</div>", "", html)
        return html

    @staticmethod
    def collapse_spaces(html: str) -> str:
        return re.sub(r"\s\s+", " ", html)

    @staticmethod
    def strip_comments(html: str) -> str:
        return re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)

    @staticmethod
    def sanitize(html: str) -> str:
        html = HTMLSanitizer.strip_comments(html)
        html = HTMLSanitizer.remove_empty_tags(html)
        html = HTMLSanitizer.collapse_spaces(html)
        return html.strip()
