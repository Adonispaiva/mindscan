# candidates_router.py — MindScan Final Version
# Adonis & Leo Vinci — 2025

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from backend.services.auth_service import AuthService
from backend.services.data_service import DataService
from backend.models import User, CandidateCreateRequest, CandidateUpdateRequest
from backend.utils.logger import logger


router = APIRouter(prefix="/candidates", tags=["Candidates"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
auth_service = AuthService()
data_service = DataService()


# =============================
# 🔐 Authentication
# =============================
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = auth_service.validate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
    return user


# =============================
# 👤 Create Candidate
# =============================
@router.post("/", summary="Criar um novo candidato")
async def create_candidate(request: CandidateCreateRequest, user: User = Depends(get_current_user)):
    logger.info(f"Usuário {user.email} criando candidato {request.full_name}.")

    try:
        candidate = await data_service.create_candidate(request)
        return {"message": "Candidato criado com sucesso", "candidate": candidate}

    except Exception as e:
        logger.error(f"Erro ao criar candidato: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar candidato")


# =============================
# 📄 List Candidates
# =============================
@router.get("/", summary="Listar todos os candidatos")
async def list_candidates(user: User = Depends(get_current_user)):
    logger.info(f"Usuário {user.email} solicitou lista de candidatos.")

    try:
        candidates = await data_service.get_all_candidates()
        return candidates

    except Exception as e:
        logger.error(f"Erro ao listar candidatos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar candidatos")


# =============================
# 🔎 Get Candidate by ID
# =============================
@router.get("/{candidate_id}", summary="Obter dados de um candidato")
async def get_candidate(candidate_id: str, user: User = Depends(get_current_user)):
    logger.info(f"Obtendo dados do candidato {candidate_id}.")

    candidate = await data_service.get_candidate(candidate_id)

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato não encontrado.")

    return candidate


# =============================
# ✏️ Update Candidate
# =============================
@router.put("/{candidate_id}", summary="Atualizar dados de um candidato")
async def update_candidate(
    candidate_id: str,
    request: CandidateUpdateRequest,
    user: User = Depends(get_current_user),
):
    logger.info(f"Atualizando candidato {candidate_id}.")

    try:
        updated = await data_service.update_candidate(candidate_id, request)

        if not updated:
            raise HTTPException(status_code=404, detail="Candidato não encontrado.")

        return {"message": "Candidato atualizado com sucesso"}

    except Exception as e:
        logger.error(f"Erro ao atualizar candidato: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar candidato")


# =============================
# 🗑️ Delete Candidate
# =============================
@router.delete("/{candidate_id}", summary="Excluir candidato")
async def delete_candidate(candidate_id: str, user: User = Depends(get_current_user)):
    logger.info(f"Removendo candidato {candidate_id}.")

    try:
        deleted = await data_service.delete_candidate(candidate_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Candidato não encontrado.")

        return {"message": "Candidato removido com sucesso"}

    except Exception as e:
        logger.error(f"Erro ao excluir candidato: {e}")
        raise HTTPException(status_code=500, detail="Erro ao excluir candidato")

