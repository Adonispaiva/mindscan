from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# IMPORTS CORRIGIDOS — compatíveis com execução a partir de /backend
from services.auth_service import AuthService
from services.data_service import DataService
from models import UserCreate, UserPublic, UserUpdate, AuthResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# =============================
#  Dependência de Autenticação
# =============================
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = AuthService.validate_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )
    return user


# =============================
#  Registro de Usuário
# =============================
@router.post("/register", response_model=UserPublic)
async def register(user: UserCreate):
    """
    Cria um novo usuário no sistema.
    """
    created = AuthService.create_user(user)
    return created


# =============================
#  Login
# =============================
@router.post("/login", response_model=AuthResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica um usuário e retorna um token JWT.
    """
    token = AuthService.authenticate(
        email=form_data.username,
        password=form_data.password
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas."
        )

    return AuthResponse(
        access_token=token,
        token_type="bearer"
    )


# =============================
#  Perfil do Usuário
# =============================
@router.get("/me", response_model=UserPublic)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Retorna o perfil do usuário autenticado.
    """
    return current_user


# =============================
#  Atualização de Perfil
# =============================
@router.put("/update", response_model=UserPublic)
async def update_user(
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza dados do usuário autenticado.
    """
    updated = DataService.update_user(current_user["id"], update_data)
    return updated


# =============================
#  Exclusão de Usuário
# =============================
@router.delete("/delete")
async def delete_user(current_user: dict = Depends(get_current_user)):
    """
    Remove permanentemente o usuário autenticado.
    """
    DataService.delete_user(current_user["id"])
    return {"status": "ok", "message": "Usuário removido com sucesso."}


# =============================
#  Lista todos os usuários — ADMIN
# =============================
@router.get("/all", response_model=list[UserPublic])
async def list_users(current_user: dict = Depends(get_current_user)):
    """
    Lista todos os usuários — somente admins.
    """

    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores."
        )

    return DataService.list_users()
