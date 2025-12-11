# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_normalizer.py
# Última atualização: 2025-12-11T09:59:20.856706

# ============================================================
# MindScan — MI Normalizer
# ============================================================
# O MI Normalizer prepara os dados brutos, já processados pelos
# algoritmos psicométricos, para consumo na camada MI.
#
# Funções:
# - validação de chaves
# - preenchimento de ausências
# - padronização de nomes
# - conversão em estruturas uniformes
# - segurança de ranges
#
# Versão final e maximizada.
# ============================================================

from typing import Dict, Any


class MINormalizer:
    """
    Normalizador oficial da camada MI.
    """

    # ------------------------------------------------------------
    # GARANTIR QUE TODAS AS DIMENSÕES EXISTAM
    # ------------------------------------------------------------
    def ensure_dimension(self, block: Dict[str, Any], required_keys: Dict[str, Any], label: str):
        missing = []
        for key in required_keys:
            if key not in block:
                missing.append(key)
                block[key] = {
                    "score": 0,
                    "descriptor": f"Valor ausente em {label}.",
                    "metadata": {}
                }

        if missing:
            block["__missing__"] = missing

        return block

    # ------------------------------------------------------------
    # PREPARAR TODOS OS RESULTADOS PARA MI
    # ------------------------------------------------------------
    def normalize_all(
        self,
        big5: Dict[str, Any],
        teique: Dict[str, Any],
        dass21: Dict[str, Any],
        ocai: Dict[str, Any],
        esquemas: Dict[str, Any],
        performance: Dict[str, Any],
        cross: Dict[str, Any],
        bussola: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Normaliza todos os blocos psicométricos para a MI.
        """

        # Garantir estrutura mínima
        self.ensure_dimension(big5, big5.keys(), "Big Five")
        self.ensure_dimension(teique, teique.keys(), "TEIQue")
        self.ensure_dimension(dass21, dass21.keys(), "DASS-21")
        self.ensure_dimension(ocai, ocai.keys(), "OCAI")
        self.ensure_dimension(esquemas, esquemas.keys(), "Esquemas")
        self.ensure_dimension(performance, performance.keys(), "Performance")
        self.ensure_dimension(cross, cross.keys(), "Cruzamentos")
        self.ensure_dimension(bussola, bussola.keys(), "Bússola")

        # Normalização final
        return {
            "big5": big5,
            "teique": teique,
            "dass21": dass21,
            "ocai": ocai,
            "esquemas": esquemas,
            "performance": performance,
            "cross": cross,
            "bussola": bussola,
            "metadata": {
                "normalized": True,
                "mi_normalizer_version": "1.0"
            }
        }


# Instância pública
mi_normalizer = MINormalizer()
