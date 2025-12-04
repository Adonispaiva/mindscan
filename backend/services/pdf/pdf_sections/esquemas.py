#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
esquemas.py — Seção de Esquemas (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
-----------------------------------------------------------
Exibe:
- Intensidade dos esquemas
- Impacto funcional
- Síntese MI
"""

from typing import Dict, Any


def build_esquemas(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial: {id, titulo, html}
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    esquemas = resultados.get("esquemas", {}) or {}
    esquemas_mi = mi.get("esquemas", {}) or {}

    texto_mi = esquemas_mi.get(
        "texto",
        "Os esquemas identificados representam padrões cognitivo-emocionais "
        "que influenciam comportamentos, decisões e relações profissionais."
    )

    # Construção das linhas da tabela
    linhas_html = []
    for nome, intensidade in esquemas.items():
        linhas_html.append(f"<tr><td>{nome}</td><td>{intensidade}</td></tr>")

    if not linhas_html:
        linhas_html.append(
            "<tr><td colspan='2'>Nenhum esquema identificado.</td></tr>"
        )

    tabela = "".join(linhas_html)

    html = f"""
<section class="esquemas page">

    <h2 class="secao-titulo">Esquemas — Padrões Cognitivo-Emocionais</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-padrao">
        <thead>
            <tr>
                <th>Esquema</th>
                <th>Intensidade</th>
            </tr>
        </thead>
        <tbody>
            {tabela}
        </tbody>
    </table>

</section>
"""

    return {
        "id": "esquemas",
        "titulo": "Esquemas — Padrões Cognitivo-Emocionais",
        "html": html
    }
