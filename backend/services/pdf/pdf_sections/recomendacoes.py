#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recomendacoes.py — Seção de Recomendações Profissionais (MindScan PDF Premium)
------------------------------------------------------------------------------

Inclui:
- Recomendações de desenvolvimento
- Sugestões práticas alinhadas aos resultados
- Direcionamentos estratégicos
- Texto moldado por MI (quando disponível)
"""

class RecomendacoesSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})
        rec_mi = mi.get("recomendacoes", {})

        texto_mi = rec_mi.get(
            "texto",
            "Com base nos padrões identificados, seguem recomendações estratégicas "
            "para fortalecimento do desempenho profissional e desenvolvimento contínuo."
        )

        lista_recs = rec_mi.get("lista", [
            "Aprimorar consistência comportamental em contextos de pressão.",
            "Desenvolver estratégias de regulação emocional.",
            "Expandir repertório de interação social em ambientes colaborativos.",
            "Fortalecer postura analítica em decisões complexas."
        ])

        itens = "".join([f"<li>{item}</li>" for item in lista_recs])

        return f"""
<section class="recomendacoes">

    <h2 class="secao-titulo">Recomendações Profissionais</h2>

    <p class="mi-texto">{texto_mi}</p>

    <ul class="lista-recomendacoes">
        {itens}
    </ul>

</section>
"""
