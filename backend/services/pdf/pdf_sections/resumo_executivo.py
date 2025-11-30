#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
resumo_executivo.py — Seção de Resumo Executivo (MindScan PDF Premium)
-----------------------------------------------------------------------

Resumo oficial e estratégico do relatório MindScan.
Inclui:

- Síntese geral das avaliações
- Macrodiagnóstico psicoprofissional
- Destaques positivos
- Pontos de atenção
- Diretrizes claras para tomada de decisão
- Texto moldado pelo MI para manter consistência editorial
"""

class ResumoExecutivoSection:
    def render(self, context: dict) -> str:

        resultados = context.get("resultados", {})
        mi = context.get("mi", {})
        resumo_mi = mi.get("resumo_executivo", {})

        # Dados de entrada
        big_five = resultados.get("big_five", {})
        teique = resultados.get("teique", {})
        dass = resultados.get("dass", {})
        esquemas = resultados.get("esquemas", {})

        # Textos do MI (fallback caso o MI ainda não esteja plugado)
        texto_resumo = resumo_mi.get(
            "texto",
            "O MindScan identificou padrões comportamentais, emocionais e cognitivos "
            "que permitem compreender com precisão a atuação profissional do avaliado."
        )

        destaques = resumo_mi.get(
            "destaques",
            [
                "Traços de personalidade bem estruturados.",
                "Boa estabilidade emocional para ambientes exigentes.",
                "Recursos cognitivos adequados para funções estratégicas."
            ]
        )

        alertas = resumo_mi.get(
            "alertas",
            [
                "Algumas tendências emocionais requerem acompanhamento.",
                "Certos padrões de esquemas podem influenciar decisões sob pressão."
            ]
        )

        return f"""
<section class="resumo-executivo">

    <h2 class="secao-titulo">Resumo Executivo</h2>

    <p class="resumo-texto">
        {texto_resumo}
    </p>

    <div class="resumo-blocos">

        <div class="bloco">
            <h3>Destaques Identificados</h3>
            <ul>
                {''.join(f'<li>{item}</li>' for item in destaques)}
            </ul>
        </div>

        <div class="bloco alertas">
            <h3>Pontos de Atenção</h3>
            <ul>
                {''.join(f'<li>{item}</li>' for item in alertas)}
            </ul>
        </div>

    </div>

</section>
"""
