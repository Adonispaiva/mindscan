# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_builder.py
# Última atualização: 2025-12-11T09:59:21.184463

# -*- coding: utf-8 -*-
"""
PDF Builder – MindScan (SynMind)
Versão definitiva – Leo Vinci v2.0
------------------------------------------------
Função:
    - Agregar *todas* as seções do MindScan
    - Gerar o pacote final de conteúdo para os renderers
    - Manter arquitetura estável, modular e expansível

O Builder NÃO toma decisões de template.
Apenas entrega o “conteúdo base” consolidado.
"""

from typing import Dict, Any, List
from pathlib import Path

# Seções padronizadas (todas convertidas no padrão {id, titulo, html})
from .pdf_sections.capa import build_capa
from .pdf_sections.identidade import build_identidade
from .pdf_sections.resumo_executivo import build_resumo_executivo
from .pdf_sections.personalidade import build_personalidade
from .pdf_sections.cultura import build_cultura
from .pdf_sections.performance import build_performance
from .pdf_sections.esquemas import build_esquemas
from .pdf_sections.dass import build_dass
from .pdf_sections.lideranca import build_lideranca
from .pdf_sections.bussola import build_bussola
from .pdf_sections.recomendacoes import build_recomendacoes
from .pdf_sections.pdi import build_pdi
from .pdf_sections.anexos import build_anexos

from .report_engine import ReportEngine
from .templates.estilo import CSS_STYLE_LOADER
from ..pdf.engine.performance_governor import PerformanceGovernor


class PDFBuilder:
    """
    Builder oficial do MindScan.
    Responsável pela coleta de seções e geração do documento bruto.
    """

    def __init__(self, payload: Dict[str, Any], template: str = "executive"):
        self.payload = payload
        self.template = template
        self.sections: List[Dict[str, Any]] = []
        self.performance_guard = PerformanceGovernor()

    # -----------------------------------------------------------
    # 1. Validação do payload
    # -----------------------------------------------------------
    def validate(self):
        """
        Validação moderna e compatível com payload MindScan v2.0.
        Regras:
            - deve conter "resultados"
            - deve conter "usuario"
            - deve conter "mi"
        Nada além disso é obrigatório.
        """
        if "resultados" not in self.payload:
            raise ValueError("[PDFBuilder] Campo obrigatório faltando: 'resultados'.")

        if "usuario" not in self.payload:
            raise ValueError("[PDFBuilder] Campo obrigatório faltando: 'usuario'.")

        if "mi" not in self.payload:
            raise ValueError("[PDFBuilder] Campo obrigatório faltando: 'mi'.")

    # -----------------------------------------------------------
    # 2. Montagem das seções
    # -----------------------------------------------------------
    def build_sections(self):
        """
        Monta TODAS as seções do MindScan.
        Renderers decidem quais usar.
        """

        self.sections = [
            build_capa(self.payload),
            build_identidade(self.payload),
            build_resumo_executivo(self.payload),
            build_personalidade(self.payload),
            build_cultura(self.payload),
            build_performance(self.payload),
            build_esquemas(self.payload),
            build_dass(self.payload),
            build_lideranca(self.payload),
            build_bussola(self.payload),
            build_recomendacoes(self.payload),
            build_pdi(self.payload),
            build_anexos(self.payload),
        ]

        return self.sections

    # -----------------------------------------------------------
    # 3. Engine de Renderização
    # -----------------------------------------------------------
    def render(self, output_path: str) -> str:
        engine = ReportEngine(template=self.template)
        css = CSS_STYLE_LOADER()
        final_doc = engine.combine(self.sections, css)
        Path(output_path).write_bytes(final_doc)
        return output_path

    # -----------------------------------------------------------
    # 4. Pipeline completo
    # -----------------------------------------------------------
    def run(self, output_path: str) -> str:
        self.performance_guard.check_start()
        self.validate()
        self.build_sections()
        pdf_path = self.render(output_path)
        self.performance_guard.check_end()
        return pdf_path
