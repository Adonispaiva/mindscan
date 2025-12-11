# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\helpers\report_utils.py
# Última atualização: 2025-12-11T09:59:21.156629

# -*- coding: utf-8 -*-
"""
MindScan — Report Utilities (Final Version)
-------------------------------------------

Glue-code oficial do módulo de Relatórios do MindScan.

Este arquivo concentra funções auxiliares essenciais para:

- Normalização de seções, blocos e summaries
- Verificação de integridade de dados enviados pela API
- Sanitização de texto contra quebras, nulls e duplicações
- Preparação de dados para renderização
- Logging simplificado
- Fallbacks seguros
- Suporte a templates

Este módulo é IMPORTANTE para garantir que o ReportService e os Renderers
recebam uma estrutura consistente e perfeita.

Inovexa Software — Arquitetura Premium.
"""

from typing import Any, Dict, List, Optional
import re
import datetime


# ----------------------------------------------------------------------
# Sanitização e Normalização
# ----------------------------------------------------------------------

def clean_text(text: Optional[str]) -> Optional[str]:
    """
    Limpa quebras excessivas, espaços sobrando e caracteres invisíveis.
    """
    if text is None:
        return None

    text = str(text).strip()
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text


def normalize_block(block: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza campos de um bloco antes de enviar ao Renderer.
    """
    block = dict(block)  # cópia defensiva

    if "title" in block:
        block["title"] = clean_text(block.get("title"))

    if "content" in block:
        block["content"] = clean_text(block.get("content"))

    if "items" in block:
        items = block.get("items") or []
        block["items"] = [clean_text(i) for i in items if i and clean_text(i)]

    # Campos de dados não são limpos (dados técnicos)
    return block


def normalize_section(section: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza uma seção inteira.
    """
    section = dict(section)

    if "title" in section:
        section["title"] = clean_text(section.get("title"))

    if "description" in section:
        section["description"] = clean_text(section.get("description"))

    blocks = section.get("blocks", [])
    section["blocks"] = [normalize_block(b) for b in blocks]

    return section


def normalize_summary(summary: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Normaliza os campos do resumo.
    """
    if not summary:
        return summary

    summary = dict(summary)

    if "headline" in summary:
        summary["headline"] = clean_text(summary.get("headline"))

    if "overview" in summary:
        summary["overview"] = clean_text(summary.get("overview"))

    if "key_points" in summary:
        kp = summary.get("key_points") or []
        summary["key_points"] = [clean_text(k) for k in kp if clean_text(k)]

    return summary


# ----------------------------------------------------------------------
# Template Helpers
# ----------------------------------------------------------------------

VALID_TEMPLATES = ["technical", "executive", "psychodynamic", "premium"]

def validate_template_name(template: str):
    """
    Verifica se o template solicitado é válido.
    """
    if template not in VALID_TEMPLATES:
        raise ValueError(
            f"Template inválido: {template}. "
            f"Use um de: {VALID_TEMPLATES}"
        )


def filter_sections_for_template(sections: List[Dict[str, Any]], template: str):
    """
    Filtra apenas as seções visíveis para o template atual.
    """
    return [
        sec for sec in sections
        if template in sec.get("visible_in", [])
    ]


# ----------------------------------------------------------------------
# Logging Simplificado
# ----------------------------------------------------------------------

def log_report_event(event: str, test_id: str, extra: Optional[Dict[str, Any]] = None):
    """
    Log de evento simples (sem dependências externas).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"[{timestamp}] [MindScan-Report] test_id={test_id} event={event}"

    if extra:
        for k, v in extra.items():
            log_line += f" {k}={v}"

    print(log_line)


# ----------------------------------------------------------------------
# Segurança e Fallbacks
# ----------------------------------------------------------------------

def safe_get(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Obtenção segura de dados de dicionário.
    """
    try:
        return d.get(key, default)
    except Exception:
        return default


def ensure_list(value: Any) -> List[Any]:
    """
    Garante que o valor seja uma lista.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


# ----------------------------------------------------------------------
# Glue Final
# ----------------------------------------------------------------------

def prepare_payload_for_render(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Limpa e normaliza TODO o payload antes de passar ao Renderer.
    """

    summary = payload.get("summary")
    sections = payload.get("sections", [])

    payload["summary"] = normalize_summary(summary)
    payload["sections"] = [normalize_section(s) for s in sections]

    return payload

