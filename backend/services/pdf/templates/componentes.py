# -*- coding: utf-8 -*-
"""
componentes.py — Biblioteca Oficial de Componentes HTML (MindScan SynMind v2.0)
Autor: Leo Vinci (Inovexa)
--------------------------------------------------------------------------------
Este módulo substitui integralmente o antigo componentes.html.

Todos os componentes abaixo são funções puras que retornam HTML
compatível com:
    - ReportEngine.combine()
    - PDFBuilder v2.0
    - Renderers v2.0 (Weasy / Async / Distributed)

Cada função deve retornar HTML final (string), SEM placeholders.
"""


# -----------------------------------------------------------------------------
# 1. FRASE DESTAQUE
# -----------------------------------------------------------------------------
def frase_destaque(texto: str) -> str:
    return f"""
    <div class="frase-destaque">
        <p>{texto}</p>
    </div>
    """


# -----------------------------------------------------------------------------
# 2. QUADRO DESTACADO (TÍTULO + CONTEÚDO)
# -----------------------------------------------------------------------------
def quadro_destaque(titulo: str, conteudo: str) -> str:
    return f"""
    <div class="quadro-destaque bloco">
        <h3>{titulo}</h3>
        <p>{conteudo}</p>
    </div>
    """


# -----------------------------------------------------------------------------
# 3. QUADRO COM LISTA
# -----------------------------------------------------------------------------
def quadro_lista(titulo: str, itens: list[str]) -> str:
    itens_html = "".join(f"<li>{item}</li>" for item in itens)
    return f"""
    <div class="quadro-destaque bloco">
        <h3>{titulo}</h3>
        <ul>
            {itens_html}
        </ul>
    </div>
    """


# -----------------------------------------------------------------------------
# 4. INDICADOR NUMÉRICO (valor + descrição)
# -----------------------------------------------------------------------------
def indicador_numerico(valor: str, descricao: str) -> str:
    return f"""
    <div class="indicador-numerico">
        <div class="valor">{valor}</div>
        <div class="descricao">{descricao}</div>
    </div>
    """


# -----------------------------------------------------------------------------
# 5. BARRA DE MÉTRICA (horizontal)
# -----------------------------------------------------------------------------
def barra_metrica(label: str, percentual: float) -> str:
    # Garantir faixa segura
    p = max(0, min(percentual, 100))

    return f"""
    <div class="metrica-linha">
        <span class="metrica-label">{label}</span>
        <div class="metrica-barra">
            <div class="metrica-preenchimento" style="width: {p}%"></div>
        </div>
        <span class="metrica-valor">{p:.0f}%</span>
    </div>
    """


# -----------------------------------------------------------------------------
# 6. TABELA PADRÃO
# -----------------------------------------------------------------------------
def tabela_padrao(colunas: list[str], linhas: list[list[str]]) -> str:
    colunas_html = "".join(f"<th>{c}</th>" for c in colunas)

    linhas_html = "".join(
        "<tr>" + "".join(f"<td>{valor}</td>" for valor in linha) + "</tr>"
        for linha in linhas
    )

    return f"""
    <table class="tabela-padrao">
        <thead>
            <tr>{colunas_html}</tr>
        </thead>
        <tbody>
            {linhas_html}
        </tbody>
    </table>
    """


# -----------------------------------------------------------------------------
# 7. BLOCO DE TEXTO PADRÃO
# -----------------------------------------------------------------------------
def bloco_texto(titulo: str, texto: str) -> str:
    return f"""
    <div class="bloco-texto">
        <h3>{titulo}</h3>
        <p>{texto}</p>
    </div>
    """


# -----------------------------------------------------------------------------
# 8. SEÇÃO GENÉRICA (usada por renderizações especiais)
# -----------------------------------------------------------------------------
def bloco_generico(html_interno: str) -> str:
    return f"""
    <div class="bloco-generico">
        {html_interno}
    </div>
    """
