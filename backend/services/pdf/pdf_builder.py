#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_builder.py — MindScan PDF Builder (Premium)
------------------------------------------------
Responsável por:
- Carregar e instanciar todas as seções do relatório
- Montar o pipeline em ordem lógica
- Criar contexto consolidado (algoritmos, MI, dados brutos)
- Integrar com o PDFEngine
"""

from pathlib import Path
from typing import Dict, Any, List

# Import das seções
from pdf_sections.capa import CapaSection
from pdf_sections.identidade import IdentidadeSection
from pdf_sections.resumo_executivo import ResumoExecutivoSection
from pdf_sections.personalidade import PersonalidadeSection
from pdf_sections.lideranca import LiderancaSection
from pdf_sections.cultura import CulturaSection
from pdf_sections.esquemas import EsquemasSection
from pdf_sections.dass import DASSSection
from pdf_sections.performance import PerformanceSection
from pdf_sections.bussola import BussolaSection
from pdf_sections.recomendacoes import RecomendacoesSection
from pdf_sections.pdi import PDISection
from pdf_sections.anexos import AnexosSection

from pdf_engine import PDFEngine


class PDFBuilder:
    """
    Orquestra o relatório completo do MindScan.
    """

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("./output")
        self.engine = PDFEngine(self.output_dir)

        # Ordem oficial das seções do relatório
        self.sections = [
            CapaSection(),
            IdentidadeSection(),
            ResumoExecutivoSection(),
            PersonalidadeSection(),
            LiderancaSection(),
            CulturaSection(),
            EsquemasSection(),
            DASSSection(),
            PerformanceSection(),
            BussolaSection(),
            RecomendacoesSection(),
            PDISection(),
            AnexosSection(),
        ]

    def build_context(self, dados_usuario: Dict[str, Any], resultados: Dict[str, Any], mi: Dict[str, Any]):
        """
        Consolida dados do usuário, algoritmos, análises e MI.
        """
        return {
            "usuario": dados_usuario,
            "resultados": resultados,
            "mi": mi,
        }

    def gerar_relatorio(self, dados_usuario: dict, resultados: dict, mi: dict, renderer):
        """
        Entrada principal para geração do relatório.
        """
        context = self.build_context(dados_usuario, resultados, mi)
        return self.engine.render(self.sections, context, renderer)
