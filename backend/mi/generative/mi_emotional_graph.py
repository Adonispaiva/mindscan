# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_emotional_graph.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIEmotionalGraph:
    """
    Constrói um grafo emocional com pesos representando intensidades,
    conexões e influências entre emoções principais.
    """

    @staticmethod
    def build(tei: dict) -> dict:
        nodes = {}
        edges = {}

        for k, v in tei.items():
            nodes[k] = v

        keys = list(tei.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]
                edges[f"{a}_{b}"] = round((tei[a] + tei[b]) / 2, 2)

        return {
            "nodes": nodes,
            "edges": edges,
            "density": len(edges)
        }
