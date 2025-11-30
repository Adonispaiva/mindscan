#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
personalidade.py — Seção de Personalidade (MindScan PDF Premium)
----------------------------------------------------------------

Esta seção apresenta:
- Radar Big Five
- Interpretações comportamentais
- Análise textual via MI
- Síntese dos padrões predominantes
"""

class PersonalidadeSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})

        big_five = resultados.get("big_five", {})
        texto_mi = mi.get("personalidade", {}).get(
            "texto",
            "A análise dos traços de personalidade revela padrões consistentes "
            "com o estilo de funcionamento predominante do avaliado."
        )

        # Construção da tabela de traços (simples)
        def linha(nome, valor):
            return f"<tr><td>{nome}</td><td>{valor}</td></tr>"

        tabela = "".join([
            linha("Abertura", big_five.get("abertura", "—")),
            linha("Conscienciosidade", big_five.get("conscienciosidade", "—")),
            linha("Extroversão", big_five.get("extroversao", "—")),
            linha("Agradabilidade", big_five.get("agradabilidade", "—")),
            linha("Estabilidade Emocional", big_five.get("neuroticismo", "—")),
        ])

        return f"""
<section class="personalidade">

    <h2 class="secao-titulo">Perfil de Personalidade (Big Five)</h2>

    <p class="mi-texto">
        {texto_mi}
    </p>

    <table class="tabela-bf">
        <thead>
            <tr>
                <th>Dimensão</th>
                <th>Percentil</th>
            </tr>
        </thead>
        <tbody>
            {tabela}
        </tbody>
    </table>

</section>
"""
