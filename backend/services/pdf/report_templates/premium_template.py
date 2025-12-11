# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\report_templates\premium_template.py
# Última atualização: 2025-12-11T09:59:21.271872

# -*- coding: utf-8 -*-
"""
technical_template.py — Template Técnico do MindScan (SynMind v2.0)
Autor: Leo Vinci (Inovexa)
---------------------------------------------------------------------------------
Função:
    Definir a ordem e composição das seções do relatório técnico do MindScan.

Este módulo NÃO produz HTML diretamente — apenas organiza as seções técnicas
que serão renderizadas posteriormente pelo PDFBuilder v2.0 + ReportEngine v2.0.
"""

from backend.services.pdf.pdf_sections.capa import build_capa
from backend.services.pdf.pdf_sections.resumo_executivo import build_resumo_executivo
from backend.services.pdf.pdf_sections.personalidade import build_personalidade
from backend.services.pdf.pdf_sections.cultura import build_cultura
from backend.services.pdf.pdf_sections.performance import build_performance
from backend.services.pdf.pdf_sections.esquemas import build_esquemas
from backend.services.pdf.pdf_sections.dass import build_dass
from backend.services.pdf.pdf_sections.lideranca import build_lideranca
from backend.services.pdf.pdf_sections.bussola import build_bussola
from backend.services.pdf.pdf_sections.recomendacoes import build_recomendacoes
from backend.services.pdf.pdf_sections.pdi import build_pdi
from backend.services.pdf.pdf_sections.anexos import build_anexos


def montar_template_tecnico(payload: dict) -> list:
    """
    Estrutura técnica oficial do MindScan SynMind v2.0.
    Retorna uma lista de dicionários contendo as seções processadas.
    """

    return [
        # Capa técnica (id visual único)
        build_capa(payload),

        # Sumário técnico (resumo de indicadores globais)
        build_resumo_executivo(payload),

        # Perfil psicológico detalhado
        build_personalidade(payload),

        # Cultura organizacional — mapa técnico e subfatores
        build_cultura(payload),

        # Performance — análise profunda de indicadores
        build_performance(payload),

        # Esquemas — análise técnica dos padrões cognitivo-comportamentais
        build_esquemas(payload),

        # Liderança — avaliação técnica dos estilos e níveis de influência
        build_lideranca(payload),

        # Bússola de Competências — análise detalhada por eixo
        build_bussola(payload),

        # DASS — indicadores técnicos de estresse, ansiedade e depressão
        build_dass(payload),

        # Recomendações técnicas — insights operacionais
        build_recomendacoes(payload),

        # Plano de Desenvolvimento Individual
        build_pdi(payload),

        # Anexos técnicos — dados complementares
        build_anexos(payload),
    ]


def get_sections(payload: dict) -> list:
    """
    Ponto de entrada padrão usado pelo PDFBuilder v2.0.
    """
    return montar_template_tecnico(payload)
