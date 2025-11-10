from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from models.user import User
from database import AsyncSessionLocal  # ✅ desacoplado de main.py

# ---------------------------------------------------------------------
# CONFIGURAÇÕES DE SEGURANÇA
# ---------------------------------------------------------------------
SECRET_KEY = "inovexa_mindscan_secret_key"  # ⚠️ usar variável de ambiente em produção
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["Auth"])

# ---------------------------------------------------------------------
# DEPENDÊNCIA DE SESSÃO
# ---------------------------------------------------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ---------------------------------------------------------------------
# SCHEMAS
# ---------------------------------------------------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ---------------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ---------------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------------------
@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Autentica um usuário e retorna um token JWT."""
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=Token)
async def register_user(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Cria novo usuário com senha criptografada e retorna token de acesso."""
    result = await db.execute(select(User).where(User.email == credentials.email))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    hashed_password = get_password_hash(credentials.password)
    new_user = User(email=credentials.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
