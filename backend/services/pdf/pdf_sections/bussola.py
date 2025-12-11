# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_sections\bussola.py
# Última atualização: 2025-12-11T09:59:21.215694

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bussola.py — Seção Bússola de Direcionamento (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
-------------------------------------------------------------------
Apresenta:
- Direcionadores profissionais
- Forças dominantes
- Alertas funcionais
- Análise narrativa via MI
"""


from typing import Dict, Any


def build_bussola(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial de seção:
    {id, titulo, html}
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    bussola = resultados.get("bussola", {}) or {}
    bussola_mi = mi.get("bussola", {}) or {}

    texto_mi = bussola_mi.get(
        "texto",
        "A Bússola do MindScan identifica direcionadores dominantes e padrões "
        "que orientam o comportamento profissional em diferentes contextos."
    )

    # Construção das linhas
    linhas_html = []
    for nome, valor in bussola.items():
        linhas_html.append(f"<tr><td>{nome}</td><td>{valor}</td></tr>")

    if not linhas_html:
        linhas_html.append(
            "<tr><td colspan='2'>Sem dados de bússola disponíveis.</td></tr>"
        )

    tabela = "".join(linhas_html)

    html = f"""
<section class="bussola page">

    <h2 class="secao-titulo">Bússola de Direcionamento</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-padrao">
        <thead>
            <tr>
                <th>Dimensão</th>
                <th>Nível</th>
            </tr>
        </thead>
        <tbody>
            {tabela}
        </tbody>
    </table>

</section>
"""

    return {
        "id": "bussola",
        "titulo": "Bússola de Direcionamento",
        "html": html
    }
