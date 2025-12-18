from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        if _is_number(x):
            return float(x)
        if isinstance(x, str):
            return float(x.strip().replace(",", "."))
    except Exception:
        pass
    return float(default)


def _clamp01(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _label_3(v01: float) -> str:
    if v01 < 0.33:
        return "baixo"
    if v01 < 0.66:
        return "medio"
    return "alto"


def _flatten_numeric(d: Any, prefix: str = "") -> List[Tuple[str, float]]:
    """
    Achata um dict/list procurando números. Retorna pares (chave_composta, valor_float).
    """
    out: List[Tuple[str, float]] = []

    if isinstance(d, dict):
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.extend(_flatten_numeric(v, key))
        return out

    if isinstance(d, list):
        for i, v in enumerate(d):
            key = f"{prefix}[{i}]"
            out.extend(_flatten_numeric(v, key))
        return out

    if _is_number(d) or isinstance(d, str):
        val = _safe_float(d, default=0.0)
        out.append((prefix or "value", val))
        return out

    return out


@dataclass(frozen=True)
class AggregatedModuleScore:
    module: str
    raw_values: Dict[str, float]
    mean: float
    min_value: float
    max_value: float
    normalized_0_1: float
    label: str


class ScoreAggregator:
    """
    Agregador determinístico:
    - Extrai valores numéricos de cada módulo
    - Calcula média/min/max por módulo
    - Normaliza para 0..1 usando escala robusta por módulo (min/max observados)
      * Se min==max, usa clamp(mean) se já estiver em 0..1, senão 0.5
    """

    def aggregate_modules(self, results: Dict[str, Any]) -> Dict[str, AggregatedModuleScore]:
        if not isinstance(results, dict):
            raise ValueError("results deve ser dict")

        aggregated: Dict[str, AggregatedModuleScore] = {}

        for module_name, module_data in results.items():
            # ignora chaves de controle
            if module_name in ("status", "results", "scores"):
                continue

            flat = _flatten_numeric(module_data)
            raw_map = {k: v for k, v in flat}

            if not raw_map:
                # módulo sem números: ainda retorna score neutro
                mean = 0.0
                mn = 0.0
                mx = 0.0
                norm = 0.5
                label = _label_3(norm)
                aggregated[module_name] = AggregatedModuleScore(
                    module=module_name,
                    raw_values={},
                    mean=mean,
                    min_value=mn,
                    max_value=mx,
                    normalized_0_1=norm,
                    label=label,
                )
                continue

            values = list(raw_map.values())
            mean = sum(values) / float(len(values))
            mn = min(values)
            mx = max(values)

            if mx == mn:
                # se já estiver em 0..1, respeita; senão neutro
                if 0.0 <= mean <= 1.0:
                    norm = _clamp01(mean)
                else:
                    norm = 0.5
            else:
                norm = _clamp01((mean - mn) / (mx - mn))

            aggregated[module_name] = AggregatedModuleScore(
                module=module_name,
                raw_values=raw_map,
                mean=mean,
                min_value=mn,
                max_value=mx,
                normalized_0_1=norm,
                label=_label_3(norm),
            )

        return aggregated

    def overall(self, aggregated: Dict[str, AggregatedModuleScore]) -> Dict[str, Any]:
        if not aggregated:
            return {
                "overall_normalized_0_1": 0.5,
                "overall_label": _label_3(0.5),
                "modules_count": 0,
            }

        norms = [m.normalized_0_1 for m in aggregated.values()]
        overall_norm = sum(norms) / float(len(norms))
        overall_norm = _clamp01(overall_norm)

        return {
            "overall_normalized_0_1": overall_norm,
            "overall_label": _label_3(overall_norm),
            "modules_count": len(aggregated),
        }
