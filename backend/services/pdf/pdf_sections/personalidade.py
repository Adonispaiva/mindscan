# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\pdf_sections\personalidade.py
# Última atualização: 2025-12-11T09:59:21.231327

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
personalidade.py — Seção de Personalidade (MindScan PDF Premium)
Versão consolidada — Leo Vinci v2.0
-----------------------------------------------------------
Apresenta:
- Radar Big Five (tabela)
- Interpretação comportamental via MI
- Síntese textual premium
"""

from typing import Dict, Any


def build_personalidade(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Padrão oficial: {id, titulo, html}
    Implementação compatível com todos os templates premium.
    """

    resultados = context.get("resultados", {})
    mi = context.get("mi", {})

    big = resultados.get("big_five", {})

    texto_mi = mi.get("personalidade", {}).get(
        "texto",
        "A análise dos traços de personalidade revela padrões consistentes "
        "com o estilo de funcionamento predominante do avaliado."
    )

    # Fallback seguro
    abertura = big.get("abertura", "—")
    consc = big.get("conscienciosidade", "—")
    extrov = big.get("extroversao", "—")
    agrad = big.get("agradabilidade", "—")
    neuro = big.get("neuroticismo", "—")

    html = f"""
<section class="personalidade page">

    <h2 class="secao-titulo">Perfil de Personalidade (Big Five)</h2>

    <p class="mi-texto">
        {texto_mi}
    </p>

    <table class="tabela-padrao">
        <thead>
            <tr>
                <th>Dimensão</th>
                <th>Percentil</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Abertura</td><td>{abertura}</td></tr>
            <tr><td>Conscienciosidade</td><td>{consc}</td></tr>
            <tr><td>Extroversão</td><td>{extrov}</td></tr>
            <tr><td>Agradabilidade</td><td>{agrad}</td></tr>
            <tr><td>Estabilidade Emocional</td><td>{neuro}</td></tr>
        </tbody>
    </table>

</section>
"""

    return {
        "id": "personalidade",
        "titulo": "Perfil de Personalidade (Big Five)",
        "html": html
    }
