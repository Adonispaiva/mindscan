# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\schemas\report_schema.py
# Última atualização: 2025-12-11T09:59:20.761538

# -*- coding: utf-8 -*-
"""
Report Schema — MindScan
------------------------

Define estruturas Pydantic para entrada e saída do módulo de relatórios.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ReportSectionBlock(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ReportSection(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    blocks: List[ReportSectionBlock] = []


class ReportSummary(BaseModel):
    headline: Optional[str] = None
    overview: Optional[str] = None
    key_points: List[str] = []


class ReportContext(BaseModel):
    name: str
    position: Optional[str] = None
    area: Optional[str] = None
    additional: Optional[Dict[str, Any]] = None


class ReportPayload(BaseModel):
    test_id: str
    context: ReportContext
    summary: Optional[ReportSummary] = None
    sections: List[ReportSection] = []


class ReportResponse(BaseModel):
    html_path: str
    pdf_path: str
