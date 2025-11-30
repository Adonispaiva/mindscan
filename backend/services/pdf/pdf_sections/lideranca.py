#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lideranca.py — Seção de Estilo de Liderança (MindScan PDF Premium)
------------------------------------------------------------------

Conteúdos fornecidos:

- Interpretação de liderança baseada em Big Five + TEIQue
- Padrões de tomada de decisão
- Estilo de influência e gestão
- Texto formatado via MI (se disponível)
- Tabela operacional de indicadores
"""

class LiderancaSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})
        lideranca_mi = mi.get("lideranca", {})

        texto_mi = lideranca_mi.get(
            "texto",
            "O estilo de liderança demonstra padrões de influência, coordenação e "
            "gestão coerentes com os traços de personalidade predominantes."
        )

        # Dados baseados em algoritmos (cada projeto pode alimentar isso de forma dinâmica)
        estilo = resultados.get("lideranca", {})

        def linha(nome, valor):
            return f"<tr><td>{nome}</td><td>{valor}</td></tr>"

        tabela = "".join([
            linha("Tomada de decisão", estilo.get("decisao", "—")),
            linha("Influência social", estilo.get("influencia", "—")),
            linha("Gestão emocional", estilo.get("gestao_emocional", "—")),
            linha("Direção e clareza", estilo.get("direcao", "—")),
            linha("Relacionamento interpessoal", estilo.get("relacional", "—")),
        ])

        return f"""
<section class="lideranca">

    <h2 class="secao-titulo">Estilo de Liderança</h2>

    <p class="mi-texto">
        {texto_mi}
    </p>

    <table class="tabela-lideranca">
        <thead>
            <tr>
                <th>Indicador</th>
                <th>Nível</th>
            </tr>
        </thead>
        <tbody>
            {tabela}
        </tbody>
    </table>

</section>
"""
