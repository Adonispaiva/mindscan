# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\graphql_live\gql_live_router.py
# Última atualização: 2025-12-11T09:59:27.667847

from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from .gql_live_schema import schema_live

router = APIRouter(prefix="/gql-live", tags=["GraphQL Live"])
router.include_router(GraphQLRouter(schema_live), prefix="")
