#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anexos.py — Seção de Anexos (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
---------------------------------------------------------------------------
Inclui:
- Tabelas e dados adicionais
- Informações complementares
- Anexos dinâmicos (texto, números, imagens base64)
"""

from typing import Dict, Any, List


def build_anexos(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial de seção:
    {id, titulo, html}
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    anexos: List[Any] = resultados.get("anexos", []) or []
    anexos_mi = mi.get("anexos", {}) or {}

    texto_mi = anexos_mi.get(
        "texto",
        "Esta seção apresenta informações complementares que enriquecem a "
        "interpretação dos resultados obtidos pelo MindScan."
    )

    # Renderização dos anexos dinâmicos
    itens_html = []

    for idx, item in enumerate(anexos, start=1):

        # Texto simples
        if isinstance(item, str):
            itens_html.append(f"<li><strong>Anexo {idx}:</strong> {item}</li>")

        # Imagens base64
        elif isinstance(item, dict) and item.get("tipo") == "imagem":
            src = item.get("base64", "")
            legenda = item.get("legenda", f"Imagem {idx}")
            itens_html.append(
                f"<li><strong>{legenda}:</strong><br><img src='{src}' "
                f"alt='{legenda}' style='max-width: 100%; margin-top: 10px;'></li>"
            )

        # Dados estruturados (listas ou dicts)
        else:
            itens_html.append(
                f"<li><strong>Anexo {idx}:</strong> Dados adicionais disponíveis.</li>"
            )

    # Fallback
    if not itens_html:
        itens_html.append("<p>Nenhum anexo adicional fornecido.</p>")

    lista_html = "<ul>" + "".join(itens_html) + "</ul>"

    html = f"""
<section class="anexos page">

    <h2 class="secao-titulo">Anexos</h2>

    <p class="mi-texto">{texto_mi}</p>

    {lista_html}

</section>
"""

    return {
        "id": "anexos",
        "titulo": "Anexos",
        "html": html
    }
