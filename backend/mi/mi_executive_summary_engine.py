# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_executive_summary_engine.py
# Última atualização: 2025-12-11T09:59:20.856706

class MIExecutiveSummaryEngine:
    """
    Gera um sumário executivo breve, objetivo e de alto impacto.
    """

    @staticmethod
    def generate(results: dict, semantic_map: dict, cross: dict) -> str:
        if not results:
            return "Não foi possível gerar o sumário executivo."

        text = []

        # Seções importantes
        main_score = results.get("global_score", "—")
        text.append(f"Desempenho Geral: {main_score}")

        if semantic_map:
            comp = semantic_map.get("competency_alignment", {})
            text.append(
                f"Alinhamento de Líderança: {comp.get('liderança', '—')}"
            )

        if cross:
            res = cross.get("resiliencia_composta")
            if res is not None:
                text.append(f"Resiliência Composta: {res}")

        return " | ".join(text)
