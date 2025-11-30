#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bussola.py — Seção Bússola de Direcionamento (MindScan PDF Premium)
-------------------------------------------------------------------

A Bússola apresenta:
- Direcionadores principais do avaliado
- Forças dominantes
- Alertas funcionais
- Análise narrativa via MI
- (Opcional) Gráfico polar, caso o renderer suporte imagens base64
"""

class BussolaSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})
        bussola_mi = mi.get("bussola", {})

        bussola = resultados.get("bussola", {})

        texto_mi = bussola_mi.get(
            "texto",
            "A Bússola do MindScan identifica direcionadores dominantes e padrões "
            "que orientam o comportamento profissional em diferentes contextos."
        )

        def linha(nome, valor):
            return f"<tr><td>{nome}</td><td>{valor}</td></tr>"

        tabela = "".join([linha(nome, valor) for nome, valor in bussola.items()]) \
            if bussola else "<tr><td colspan='2'>Sem dados de bússola</td></tr>"

        return f"""
<section class="bussola">

    <h2 class="secao-titulo">Bússola de Direcionamento</h2>

    <p class="mi-texto">{texto_mi}</p>

    <table class="tabela-bussola">
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
