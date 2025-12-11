# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\graphql\graphql_schema.py
# Última atualização: 2025-12-11T09:59:27.839711

import strawberry

@strawberry.type
class Query:
    health: str = "GraphQL Online"

schema = strawberry.Schema(query=Query)
