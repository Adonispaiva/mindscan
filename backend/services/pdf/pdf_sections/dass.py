#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dass.py — Seção DASS-21 (MindScan PDF Premium)
-----------------------------------------------
Exibe:
- Níveis de Depressão, Ansiedade e Estresse
- Classificação por faixas (leve, moderado, severo)
- Texto interpretativo com MI (se disponível)
"""

class DASSSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})
        dass_mi = mi.get("dass", {})

        dass = resultados.get("dass", {})

        texto_mi = dass_mi.get(
            "texto",
            "A avaliação DASS-21 identifica níveis emocionais relacionados a depressão, "
            "ansiedade e estresse, permitindo compreender como o avaliado responde a "
            "pressões e demandas do ambiente profissional."
        )

        def linha(nome, valor):
            return f"<tr><td>{nome}</td><td>{valor}</td></tr>"

        tabela = "".join([
            linha("Depressão", dass.get("depressao", "—")),
            linha("Ansiedade", dass.get("ansiedade", "—")),
            linha("Estresse", dass.get("estresse", "—")),
        ])

        return f"""
<section class="dass">

    <h2 class="secao-titulo">DASS-21 — Estresse, Ansiedade e Depressão</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-dass">
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
""" }