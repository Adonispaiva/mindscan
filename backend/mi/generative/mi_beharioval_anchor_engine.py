# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_beharioval_anchor_engine.py
# Última atualização: 2025-12-11T09:59:20.887954

class MIBehavioralAnchorEngine:
    """
    Identifica os “pilares comportamentais” mais estáveis do indivíduo.
    """

    @staticmethod
    def anchors(results: dict) -> dict:
        big5 = results.get("big5", {})
        sorted_traits = dict(sorted(big5.items(), key=lambda x: x[1], reverse=True))
        anchors = list(sorted_traits.keys())[:2]

        return {
            "anchors": anchors,
            "anchor_strength": {a: big5[a] for a in anchors}
        }
