# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_templates\corporate_renderer_loader.py
# Última atualização: 2025-12-11T09:59:21.292589

# -*- coding: utf-8 -*-
"""
corporate_renderer_loader.py
----------------------------

Responsável por registrar, localizar e instanciar os renderers
utilizados pelo MindScan Corporate. Este módulo permite que novos modelos
de renderização sejam adicionados futuramente sem alterar o código-base,
seguindo arquitetura plugável.

Integração atual:
- CorporateRenderer (principal renderizador corporativo)
- Pode futuramente incluir PremiumRenderer, ExecutiveRenderer etc.
"""

from typing import Dict, Any, Type

from services.report_templates.corporate_renderer import CorporateRenderer


class CorporateRendererLoader:
    """
    Loader modular para renderers. Permite expansão e substituição.
    """

    _REGISTERED_RENDERERS: Dict[str, Type] = {
        "corporate": CorporateRenderer,
    }

    @classmethod
    def register(cls, name: str, renderer_class: Type):
        """
        Registra um novo renderer no sistema.
        """
        cls._REGISTERED_RENDERERS[name] = renderer_class

    @classmethod
    def get_renderer(cls, name: str):
        """
        Recupera um renderer registrado.
        """
        renderer = cls._REGISTERED_RENDERERS.get(name)
        if not renderer:
            raise ValueError(f"Renderer '{name}' não está registrado.")
        return renderer

    @classmethod
    def instantiate(cls, name: str, payload: Dict[str, Any], html_path: str, pdf_path: str):
        """
        Instancia o renderer solicitado.
        """
        renderer_class = cls.get_renderer(name)

        return renderer_class(
            payload=payload,
            output_html=html_path,
            output_pdf=pdf_path
        )
