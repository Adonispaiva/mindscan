"""
MindScan - Base Algorithm
Path (Windows): D:\projetos-inovexa\mindscan\core\algorithms\base_algorithm.py

Objetivo
--------
Fornecer uma análise "base" estável, sem dependências externas, para validar
o pipeline do MindScan (API /mindscan/run).

Contrato
--------
- Entrada: dict (normalmente vindo do body JSON do POST), aceitando:
    {"data": {...}}  ou  {...} diretamente.
- Saída: dict JSON-serializável.

Observação
----------
Este arquivo NÃO define classe BaseAlgorithm. Ele expõe a função `run()`,
que é o padrão mais simples e robusto para o pipeline atual.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from collections import Counter
import re
from typing import Any, Dict, List, Tuple


# --- Stopwords mínimas (PT-BR + EN) para extração de keywords ---
_STOPWORDS = {
    # PT
    "a","o","os","as","um","uma","uns","umas","de","da","do","das","dos","em","no","na","nos","nas",
    "e","ou","mas","por","para","pra","com","sem","que","quem","quando","onde","como","porque","porquê",
    "eu","tu","ele","ela","nós","vos","eles","elas","me","te","se","lhe","lhes","minha","meu","meus","minhas",
    "sua","seu","seus","suas","nossa","nosso","nossos","nossas","isso","isto","aquilo","aqui","ali","lá",
    "já","não","sim","também","muito","pouco","mais","menos","só","tambem","voce","você","vocês",
    # EN
    "the","a","an","and","or","but","to","of","in","on","for","with","without","is","are","was","were","be",
    "i","you","he","she","we","they","me","my","your","yours","his","her","our","ours","their","theirs",
}

_POSITIVE = {
    "bom","boa","ótimo","otimo","excelente","legal","feliz","satisfeito","satisfeita","tranquilo",
    "positivo","ótima","otima","maravilhoso","maravilhosa","perfeito","perfeita",
}
_NEGATIVE = {
    "ruim","péssimo","pessimo","horrível","horrivel","triste","ansioso","ansiosa","raiva","medo",
    "negativo","problema","erro","falha","stress","estresse","cansado","cansada",
}


@dataclass(frozen=True)
class _ParsedInput:
    text: str
    user_id: str
    timestamp: str  # ISO-8601


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _coerce_str(v: Any, default: str = "") -> str:
    if v is None:
        return default
    if isinstance(v, str):
        return v
    return str(v)


def _parse_timestamp(ts: Any) -> str:
    """
    Aceita:
      - ISO-8601 str
      - datetime
      - None -> now()
    Retorna ISO-8601 (UTC quando possível).
    """
    if ts is None or ts == "":
        return _now_iso()

    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ts.astimezone(timezone.utc).isoformat()

    s = _coerce_str(ts).strip()
    try:
        s_norm = s.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s_norm)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return _now_iso()


def _extract_payload(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza:
      - {"data": {...}}  -> {...}
      - {...}            -> {...}
    """
    if not isinstance(input_data, dict):
        return {}
    data = input_data.get("data")
    return data if isinstance(data, dict) else input_data


def _tokenize(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+", text.lower())
    return tokens


def _sentences(text: str) -> List[str]:
    parts = re.split(r"[.!?]+", text)
    return [p.strip() for p in parts if p.strip()]


def _top_keywords(tokens: List[str], top_n: int = 8) -> List[Tuple[str, int]]:
    filtered = [t for t in tokens if t not in _STOPWORDS and len(t) >= 3]
    return Counter(filtered).most_common(top_n)


def _sentiment_score(tokens: List[str]) -> Dict[str, Any]:
    pos = sum(1 for t in tokens if t in _POSITIVE)
    neg = sum(1 for t in tokens if t in _NEGATIVE)
    score = pos - neg
    label = "neutral"
    if score >= 2:
        label = "positive"
    elif score <= -2:
        label = "negative"
    return {"label": label, "score": score, "positive_hits": pos, "negative_hits": neg}


def _basic_metrics(text: str, tokens: List[str]) -> Dict[str, Any]:
    chars = len(text)
    words = len(tokens)
    uniq = len(set(tokens))
    avg_word_len = (sum(len(t) for t in tokens) / words) if words else 0.0
    sents = _sentences(text)
    avg_sent_len = (words / len(sents)) if sents else 0.0
    return {
        "char_count": chars,
        "word_count": words,
        "unique_word_count": uniq,
        "avg_word_len": round(avg_word_len, 3),
        "sentence_count": len(sents),
        "avg_sentence_len_words": round(avg_sent_len, 3),
    }


def _language_hint(tokens: List[str]) -> str:
    if not tokens:
        return "unknown"
    pt_hits = sum(1 for t in tokens if t in {"de","do","da","que","não","sim","para","com","você","voce"})
    en_hits = sum(1 for t in tokens if t in {"the","and","to","of","in","for","with","you"})
    if pt_hits > en_hits:
        return "pt"
    if en_hits > pt_hits:
        return "en"
    return "unknown"


def _parse_input(input_data: Dict[str, Any]) -> _ParsedInput:
    payload = _extract_payload(input_data)

    text = _coerce_str(payload.get("text", "")).strip()
    user_id = _coerce_str(payload.get("user_id", "anonymous")).strip() or "anonymous"
    timestamp = _parse_timestamp(payload.get("timestamp"))

    return _ParsedInput(text=text, user_id=user_id, timestamp=timestamp)


def run(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executa a análise base.

    Entrada:
      {"data": {"text": "...", "user_id": "...", "timestamp": "..."}}
      ou
      {"text": "...", "user_id": "...", "timestamp": "..."}
    """
    parsed = _parse_input(input_data)
    tokens = _tokenize(parsed.text)

    metrics = _basic_metrics(parsed.text, tokens)
    sentiment = _sentiment_score(tokens)
    keywords = _top_keywords(tokens, top_n=10)
    lang = _language_hint(tokens)

    return {
        "algorithm": "base",
        "received_text": parsed.text,
        "user_id": parsed.user_id,
        "timestamp": parsed.timestamp,
        "language_hint": lang,
        "metrics": metrics,
        "sentiment": sentiment,
        "keywords": [{"term": k, "count": c} for k, c in keywords],
    }
