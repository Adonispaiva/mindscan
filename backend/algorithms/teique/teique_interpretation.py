# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\teique\teique_interpretation.py
# Última atualização: 2025-12-11T09:59:20.730228

from fastapi import HTTPException, status
from backend.schemas.user_schema import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
    UserListResponse,
)
from backend.database.repositories.user_repository import UserRepository


class UserService:
    """
    Serviço responsável pela gestão de usuários do BitLinker.

    Responsabilidades:
    - CRUD completo
    - Busca por ID e por e-mail
    - Integração com autenticação
    - Validações formais
    - Suporte ao painel Next.js
    - Zero lógica de UI
    """

    def __init__(self):
        self.repo = UserRepository()

    # ----------------------------------------------------------------------
    # GET LIST
    # ----------------------------------------------------------------------

    async def list_users(self, page: int, page_size: int) -> UserListResponse:
        items, total = await self.repo.list_users(page, page_size)
        return UserListResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=items,
        )

    # ----------------------------------------------------------------------
    # GET
    # ----------------------------------------------------------------------

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.repo.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )
        return user

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        return await self.repo.get_user_by_email(email)

    # ----------------------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------------------

    async def create_user(self, data: UserCreateRequest) -> UserResponse:
        # Verifica se e-mail já existe
        existing = await self.repo.get_user_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado.",
            )
        return await self.repo.create_user(data)

    # ----------------------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------------------

    async def update_user(self, user_id: int, data: UserUpdateRequest) -> UserResponse:
        updated = await self.repo.update_user(user_id, data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )
        return updated

    # ----------------------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------------------

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.repo.delete_user(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )
