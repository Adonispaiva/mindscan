# -*- coding: utf-8 -*-
"""
enterprise_template.py — Template Enterprise MindScan (SynMind v2.0)
Autor: Leo Vinci (Inovexa)
---------------------------------------------------------------------------------
Função:
    Estruturar o relatório corporativo/organizacional do MindScan.

Este template é usado em contextos empresariais:
    - Diagnóstico de equipes
    - Análise organizacional
    - Liderança executiva
    - Estruturas hierárquicas
    - Projetos Enterprise & Consultoria Premium
"""

# Seções padrão (a base da arquitetura)
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


def montar_template_enterprise(payload: dict) -> list:
    """
    Template Enterprise MindScan.
    
    A ordem é otimizada para diretoria, RH e consultorias:
    visão → estrutura psicológica → impacto organizacional → recomendações.
    """
    secoes = [
        # Identidade premium da capa corporativa
        build_capa(payload),

        # Painel executivo de abertura
        build_resumo_executivo(payload),

        # Perfil psicológico aplicado ao contexto organizacional
        build_personalidade(payload),

        # Cultura — impacto no ambiente, times e clima
        build_cultura(payload),

        # Performance — impacto comportamental em entregas
        build_performance(payload),

        # Esquemas — padrões internos que influenciam o ambiente corporativo
        build_esquemas(payload),

        # Liderança — leitura funcional e estruturada
        build_lideranca(payload),

        # Bússola — competências aplicadas a papéis e funções
        build_bussola(payload),

        # DASS — indicadores emocionais com impacto no trabalho
        build_dass(payload),

        # Recomendações organizacionais
        build_recomendacoes(payload),

        # PDI — orientado ao desenvolvimento profissional
        build_pdi(payload),

        # Anexos — materiais complementares
        build_anexos(payload),
    ]

    return secoes


def get_sections(payload: dict) -> list:
    """Ponto de entrada padrão do PDFBuilder v2.0."""
    return montar_template_enterprise(payload)
