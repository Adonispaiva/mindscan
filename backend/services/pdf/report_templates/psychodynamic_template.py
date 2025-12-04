# -*- coding: utf-8 -*-
"""
psychodynamic_template.py — Template Psicodinâmico do MindScan (SynMind v2.0)
Autor: Leo Vinci (Inovexa)
---------------------------------------------------------------------------------
Função:
    Definir a organização das seções do relatório psicodinâmico.

Este template aprofunda o eixo subjetivo, intrapsíquico e narrativo.
É usado em análises clínicas, executivas de alta complexidade e perfis de risco.
"""

# Seções padrão
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


def montar_template_psicodinamico(payload: dict) -> list:
    """
    Estrutura psicodinâmica oficial do SynMind v2.0.
    Mistura seções padrão com ênfase maior nos blocos profundos.
    """

    secoes = [
        # Capa psicodinâmica
        build_capa(payload),

        # Abertura profunda e contextual
        build_resumo_executivo(payload),

        # Perfil psicológico com ênfase dinâmica
        build_personalidade(payload),

        # Cultura — leitura simbólica e de sistemas
        build_cultura(payload),

        # Performance — explicação comportamental de resultados
        build_performance(payload),

        # Esquemas — aqui é onde o psicodinâmico ganha profundidade
        build_esquemas(payload),

        # Liderança — leitura intrapsíquica de estilos
        build_lideranca(payload),

        # Bússola — interpretação mais interpretativa e narrativa
        build_bussola(payload),

        # DASS — impacto emocional e regulação afetiva
        build_dass(payload),

        # Recomendações psicodinâmicas (implicações e dinâmicas)
        build_recomendacoes(payload),

        # PDI — foco em processos internos e autoeficácia
        build_pdi(payload),

        # Anexos — materiais complementares
        build_anexos(payload),
    ]

    return secoes


def get_sections(payload: dict) -> list:
    """
    Entrada padrão do PDFBuilder v2.0.
    """
    return montar_template_psicodinamico(payload)
