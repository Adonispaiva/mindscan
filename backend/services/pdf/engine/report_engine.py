# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\engine\report_engine.py
# Última atualização: 2025-12-11T09:59:21.200087

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_engine.py — MindScan Report Engine (SynMind v2.0)
Autor: Leo Vinci (Inovexa)
----------------------------------------------------------
Função central:
- Combinar TODAS as seções geradas pelo PDFBuilder
- Injetar o CSS premium
- Inserir o template-base
- Preparar a saída HTML final (antes da conversão para PDF)

Este engine é independente dos renderers:
    - executive_renderer
    - technical_renderer
    - psychodynamic_renderer
    - premium_renderer

Cada renderer decide quais seções usar.
Este engine apenas une tudo com coerência e estilo.
"""

from typing import List, Dict, Any


class ReportEngine:
    """
    Núcleo unificador de relatórios MindScan.
    Recebe:
        - lista de seções padronizadas ({id, titulo, html})
        - CSS premium
    Retorna:
        - HTML final renderizado para PDF
    """

    def __init__(self, template: str = "executive"):
        self.template = template

    # -----------------------------------------------------------
    # Template-base unificado (v2.0)
    # -----------------------------------------------------------
    def _base_template(self, css: str, content: str) -> str:
        """
        Template-base oficial MindScan Premium.

        Os renderers podem sobrescrever ESTE TEMPLATE
        para temas específicos de relatório — mas NUNCA
        alteram a lógica de montagem.
        """
        return f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Relatório MindScan — {self.template.title()}</title>
    <style>
        {css}
    </style>
</head>
<body class="mindscan-relatorio">
    {content}
</body>
</html>
        """

    # -----------------------------------------------------------
    # Combinação das seções
    # -----------------------------------------------------------
    def combine(self, sections: List[Dict[str, Any]], css: str) -> bytes:
        """
        Recebe as seções já montadas e produz o HTML final.
        Cada seção já contém HTML pronto.
        """
        html_sections = []

        for sec in sections:
            try:
                html_sections.append(sec["html"])
            except Exception as e:
                raise ValueError(
                    f"[ReportEngine] Seção inválida detectada: {sec}. "
                    f"Erro: {e}"
                )

        content = "\n\n".join(html_sections)
        final_html = self._base_template(css, content)

        return final_html.encode("utf-8")
