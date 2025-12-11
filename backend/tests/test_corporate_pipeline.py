# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\tests\test_corporate_pipeline.py
# Última atualização: 2025-12-11T09:59:21.292589

# -*- coding: utf-8 -*-
"""
test_corporate_pipeline.py
--------------------------

Teste de integração para validar o pipeline corporativo completo.
"""

from services.report_pipeline_helper import ReportPipelineHelper


def test_pipeline_basic():
    payload = {
        "test_id": "ABC123",
        "context": {"name": "João", "position": "Gerente"},
    }

    result = ReportPipelineHelper.prepare_for_corporate_renderer(payload)

    assert "summary" in result
    assert "sections" in result
    assert len(result["sections"]) >= 5
    assert result["summary"]["headline"] != ""
    assert result["context"]["name"] == "João"
