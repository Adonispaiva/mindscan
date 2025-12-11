# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\coaching_v4\builder\coaching_action_plan_builder.py
# Última atualização: 2025-12-11T09:59:27.542857

class CoachingActionPlanBuilder:
    """
    Constrói planos de ação de coaching automatizado.
    """

    @staticmethod
    def build(goal: str, tasks: list):
        return {
            "goal": goal,
            "tasks": tasks
        }
