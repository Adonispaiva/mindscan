# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tests\test_pdf_engine.py
# Última atualização: 2025-12-11T09:59:27.761619

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_pdf_engine.py — Testes principais do MindScan PDF Engine
-------------------------------------------------------------

Cobre:
- Validador de dados (MindScanDataValidator)
- Pipeline do PDFBuilder com renderer mock
- Carregamento básico dos templates
"""

import json
from pathlib import Path
import pytest

from backend.services.pdf.validators.data_validator import MindScanDataValidator
from pdf_builder import PDFBuilder


# ================================================================
# FIXTURES
# ================================================================
@pytest.fixture
def usuario_ok():
    return {
        "nome": "João Teste",
        "cargo": "Analista",
        "idade": 30
    }


@pytest.fixture
def resultados_ok():
    return {
        "big_five": {
            "abertura": 50,
            "conscienciosidade": 60,
            "extroversao": 40,
            "agradabilidade": 70,
            "neuroticismo": 30,
        },
        "dass": {"depressao": "Normal", "ansiedade": "Leve", "estresse": "Moderado"},
        "esquemas": {"Autoexigência": "Moderado"},
    }


@pytest.fixture
def mi_ok():
    return {"resumo_executivo": {"texto": "Tudo correto."}}


# ================================================================
# TESTE 1 — VALIDADOR
# ================================================================
def test_validator_ok(usuario_ok, resultados_ok, mi_ok):
    validator = MindScanDataValidator()
    assert validator.validar(usuario_ok, resultados_ok, mi_ok) is True


def test_validator_falha_usuario():
    validator = MindScanDataValidator()
    usuario_ruim = {"cargo": "Dev"}  # faltando nome

    with pytest.raises(ValueError):
        validator.validar(usuario_ruim, {"big_five": {}, "dass": {}, "esquemas": {}}, {})


def test_validator_falha_big_five():
    validator = MindScanDataValidator()
    resultados = {
        "big_five": {"abertura": 10},  # faltam 4 dimensões
        "dass": {},
        "esquemas": {}
    }

    with pytest.raises(ValueError):
        validator.validar({"nome": "X", "cargo": "Y"}, resultados, {})


# ================================================================
# TESTE 2 — PDFBUILDER (Mock de Renderer)
# ================================================================
class RendererMock:
    """
    Mock do renderer real.
    Em vez de gerar PDF, apenas registra o conteúdo recebido.
    """
    def __init__(self):
        self.output = None

    def render_html_to_pdf(self, conteudo_html: str, output_path: Path):
        self.output = conteudo_html
        output_path.write_text("PDF_SIMULADO", encoding="utf-8")
        return output_path


def test_pdfbuilder_pipeline(usuario_ok, resultados_ok, mi_ok, tmp_path):
    renderer = RendererMock()
    builder = PDFBuilder()

    pdf_path = builder.gerar_relatorio(
        usuario_ok,
        resultados_ok,
        mi_ok,
        renderer,
        output_path=tmp_path / "teste.pdf"
    )

    # Verifica se o PDF falso foi criado
    assert pdf_path.exists()
    assert pdf_path.read_text(encoding="utf-8") == "PDF_SIMULADO"

    # Verifica se o HTML gerado foi enviado ao renderer
    assert "<section" in renderer.output.lower()  # HTML básico presente


# ================================================================
# TESTE 3 — Templates
# ================================================================
def test_templates_existem():
    ROOT = Path(__file__).resolve().parent.parent
    templates = ROOT / "backend" / "services" / "pdf" / "templates"

    assert (templates / "base.html").exists()
    assert (templates / "estilo.css").exists()
    assert (templates / "componentes.html").exists()
