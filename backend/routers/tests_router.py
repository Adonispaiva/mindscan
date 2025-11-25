# ============================================================
# MindScan — Tests Router
# ============================================================
# Controle das sessões de teste MindScan
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_session
from backend import models

router = APIRouter()


# ------------------------------------------------------------
# CREATE TEST SESSION
# ------------------------------------------------------------
@router.post("/create")
async def create_test(
        user_id: int,
        candidate_id: int,
        session: AsyncSession = Depends(get_session)
):
    # Verifica se usuário existe
    user_result = await session.execute(
        select(models.User).where(models.User.id == user_id)
    )
    if not user_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")

    # Verifica se candidato existe
    cand_result = await session.execute(
        select(models.Candidate).where(models.Candidate.id == candidate_id)
    )
    if not cand_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Criação do teste
    test = models.MindscanTest(
        user_id=user_id,
        candidate_id=candidate_id
    )

    session.add(test)
    await session.commit()
    await session.refresh(test)

    return {
        "status": "created",
        "test_id": test.id
    }


# ------------------------------------------------------------
# LIST ALL TESTS
# ------------------------------------------------------------
@router.get("/")
async def list_tests(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.MindscanTest))
    return result.scalars().all()


# ------------------------------------------------------------
# GET TEST BY ID
# ------------------------------------------------------------
@router.get("/{test_id}")
async def get_test(test_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.MindscanTest).where(models.MindscanTest.id == test_id)
    )
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    return test


# ------------------------------------------------------------
# UPDATE STATUS OF TEST
# ------------------------------------------------------------
@router.patch("/{test_id}/status")
async def update_status(
        test_id: int,
        status: str,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(models.MindscanTest).where(models.MindscanTest.id == test_id)
    )
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    test.status = status
    await session.commit()
    await session.refresh(test)

    return {"status": "updated", "test_id": test_id, "new_status": status}


# ------------------------------------------------------------
# DELETE TEST
# ------------------------------------------------------------
@router.delete("/{test_id}")
async def delete_test(test_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(models.MindscanTest).where(models.MindscanTest.id == test_id)
    )
    test = result.scalar_one_or_none()

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    await session.delete(test)
    await session.commit()

    return {"status": "deleted", "test_id": test_id}
