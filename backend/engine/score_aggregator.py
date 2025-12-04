# MindScan Score Aggregator — Ultra Superior
# Função: unificar, normalizar e consolidar scores de múltiplos engines.

from backend.engine.normalizer import Normalizer
from backend.engine.validator import Validator

class ScoreAggregator:

    def __init__(self):
        self.normalizer = Normalizer()
        self.validator = Validator()

    def merge(self, score_maps):
        """Recebe lista de dicionários com scores e consolida tudo em um só mapa."""

        self.validator.ensure_list(score_maps)

        merged = {}
        for smap in score_maps:
            self.validator.ensure_numeric_map(smap)
            for k, v in smap.items():
                merged.setdefault(k, []).append(v)

        final = {k: sum(vs) / len(vs) for k, vs in merged.items()}
        normalized = self.normalizer.scale_range(final, 0, 100)

        return {
            "raw": final,
            "normalized": normalized,
            "count_sources": len(score_maps),
        }
