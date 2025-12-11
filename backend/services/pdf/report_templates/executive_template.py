# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\report_templates\executive_template.py
# Última atualização: 2025-12-11T09:59:21.266858

# -*- coding: utf-8 -*-
"""
executive_template.py — Template Executivo do MindScan (SynMind v2.0)
Autor: Leo Vinci (Inovexa)
-------------------------------------------------------------------------------
Função:
    Definir a **ordem oficial das seções** do Relatório Executivo MindScan.

Este arquivo NÃO gera HTML.
Ele apenas informa ao PDFBuilder quais blocos devem ser renderizados,
em qual ordem, e com quais dados.

As seções são funções Python localizadas em:
    backend/services/pdf/pdf_sections/
"""

from backend.services.pdf.pdf_sections.capa import build_capa
from backend.services.pdf.pdf_sections.resumo_executivo import build_resumo_executivo
from backend.services.pdf.pdf_sections.personalidade import build_personalidade
from backend.services.pdf.pdf_sections.cultura import build_cultura
from backend.services.pdf.pdf_sections.performance import build_performance
from backend.services.pdf.pdf_sections.esquemas import build_esquemas
from backend.services.pdf.pdf_sections.lideranca import build_lideranca
from backend.services.pdf.pdf_sections.bussola import build_bussola
from backend.services.pdf.pdf_sections.dass import build_dass
from backend.services.pdf.pdf_sections.recomendacoes import build_recomendacoes
from backend.services.pdf.pdf_sections.pdi import build_pdi
from backend.services.pdf.pdf_sections.anexos import build_anexos


def montar_template_executivo(payload: dict) -> list:
    """
    Retorna a sequência de seções que formarão o relatório executivo final.

    Cada item da lista é um dicionário retornado por build_xxx():
        {
            "id": "...",
            "titulo": "...",
            "html": "<div>...</div>"
        }
    """

    return [
        build_capa(payload),
        build_resumo_executivo(payload),
        build_personalidade(payload),
        build_cultura(payload),
        build_performance(payload),
        build_esquemas(payload),
        build_lideranca(payload),
        build_bussola(payload),
        build_dass(payload),
        build_recomendacoes(payload),
        build_pdi(payload),
        build_anexos(payload),
    ]


# Ponto de entrada padrão usado pelo PDFBuilder
def get_sections(payload: dict) -> list:
    return montar_template_executivo(payload)
