#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
performance.py — Seção de Performance (MindScan PDF Premium)
-------------------------------------------------------------

Exibe:
- Evolução de performance (trimestres, semestres ou períodos configurados)
- Indicadores numéricos e qualitativos
- Análises MI (se disponíveis)
- Possibilidade de gráficos (caso o renderer use imagens base64)
"""

class PerformanceSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})
        performance_mi = mi.get("performance", {})

        performance = resultados.get("performance", {})

        texto_mi = performance_mi.get(
            "texto",
            "A análise de performance indica tendências de evolução, estabilidade e "
            "pontos críticos que influenciam diretamente o funcionamento profissional."
        )

        # Geração de tabela simples
        linhas = []
        for periodo, valor in performance.items():
            linhas.append(f"<tr><td>{periodo}</td><td>{valor}</td></tr>")
        tabela = "".join(linhas) if linhas else "<tr><td colspan='2'>Sem dados de performance</td></tr>"

        return f"""
<section class="performance">

    <h2 class="secao-titulo">Performance — Evolução e Tendências</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-performance">
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
