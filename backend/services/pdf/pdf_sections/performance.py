# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_sections\performance.py
# Última atualização: 2025-12-11T09:59:21.231327

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
performance.py — Seção de Performance (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
-------------------------------------------------------------
Exibe:
- Evolução de performance por período
- Indicadores quantitativos
- Síntese MI da trajetória
"""

from typing import Dict, Any


def build_performance(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial de seção:
    {id, titulo, html}
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    performance = resultados.get("performance", {}) or {}
    performance_mi = mi.get("performance", {}) or {}

    texto_mi = performance_mi.get(
        "texto",
        "A análise de performance indica tendências de evolução, estabilidade e "
        "pontos críticos que influenciam diretamente o funcionamento profissional."
    )

    # Geração de linhas de tabela
    linhas_html = []
    for periodo, valor in performance.items():
        linhas_html.append(f"<tr><td>{periodo}</td><td>{valor}</td></tr>")

    if not linhas_html:
        linhas_html.append(
            "<tr><td colspan='2'>Sem dados de performance disponíveis para os períodos configurados.</td></tr>"
        )

    tabela = "".join(linhas_html)

    html = f"""
<section class="performance page">

    <h2 class="secao-titulo">Performance — Evolução e Tendências</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-padrao">
        <thead>
            <tr>
                <th>Período</th>
                <th>Indicador</th>
            </tr>
        </thead>
        <tbody>
            {tabela}
        </tbody>
    </table>

</section>
"""

    return {
        "id": "performance",
        "titulo": "Performance — Evolução e Tendências",
        "html": html
    }
