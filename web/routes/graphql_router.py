# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\routes\graphql_router.py
# Última atualização: 2025-12-11T09:59:27.855343

from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from ..graphql.graphql_schema import schema

router = APIRouter(prefix="/graphql", tags=["GraphQL"])
router.include_router(GraphQLRouter(schema), prefix="")
