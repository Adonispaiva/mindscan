# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\post_processors\corporate_post_processor.py
# Última atualização: 2025-12-11T09:59:21.276887

# -*- coding: utf-8 -*-
"""
corporate_post_processor.py
---------------------------

Aplicado após a construção do HTML e antes da geração do PDF.
Responsável por:
- Limpeza final
- Ajustes de compatibilidade
- Regras corporativas de formatação
"""

from typing import Dict
from services.adapters.corporate_render_adapter import CorporateRenderAdapter


class CorporatePostProcessor:

    @staticmethod
    def finalize(html: str) -> str:
        """
        Aplica todas as transformações necessárias para o HTML final
        ficar 100% adequado ao CorporateRenderer.
        """
        html = CorporateRenderAdapter.prepare_html(html)

        # Regras finais de pós-processamento
        html = html.replace("<br><br><br>", "<br><br>")
        html = html.replace("<!--EMPTY-->", "")

        return html
