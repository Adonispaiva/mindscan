#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estilo.py — CSS Loader Oficial do MindScan (SynMind v2.0)
Autor: Leo Vinci (Inovexa)
------------------------------------------------------------------------------
Função:
    - Carregar o conteúdo do arquivo estilo.css
    - Servir o CSS como string para o ReportEngine e renderers v2.0

Motivos:
    - CSS não deve ser lido diretamente pelos renderers
    - Torna o estilo versionado e seguro
    - Padroniza o carregamento entre pipelines síncronos e assíncronos
"""

from pathlib import Path


def CSS_STYLE_LOADER() -> str:
    """
    Carrega o estilo premium do MindScan diretamente do arquivo estilo.css.
    Retorna o CSS como string.
    """

    # Caminho padrão do arquivo de estilo
    css_path = (
        Path(__file__)
        .resolve()
        .parent
        .joinpath("estilo.css")
    )

    if not css_path.exists():
        raise FileNotFoundError(
            f"[CSS_STYLE_LOADER] Arquivo de estilo não encontrado: {css_path}"
        )

    try:
        return css_path.read_text(encoding="utf-8")

    except Exception as e:
        raise RuntimeError(
            f"[CSS_STYLE_LOADER] Falha ao carregar estilo.css: {e}"
        )
