# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\graphql_live\subscriptions\gql_subscription_manager.py
# Última atualização: 2025-12-11T09:59:27.683474

class GQLSubscriptionManager:
    """
    Gerencia subscriptions GraphQL em tempo real.
    """

    subscribers = []

    @staticmethod
    def subscribe(client_id: str):
        GQLSubscriptionManager.subscribers.append(client_id)
        return {"subscribed": client_id}

    @staticmethod
    def broadcast(event: dict):
        return {
            "broadcasted_to": GQLSubscriptionManager.subscribers,
            "event": event
        }
