from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import require_role
from app.database.models import AuditLog, Document, EvaluationRun, User, UserRole
from app.database.postgres import get_db
from app.rag.evaluation.ragas_eval import run_evaluation

router = APIRouter(prefix="/admin", tags=["admin"])


class DashboardStats(BaseModel):
    total_users: int
    total_documents: int
    indexed_documents: int
    total_evaluations: int


class EvalRequest(BaseModel):
    dataset_name: str = "sample"


@router.get("/stats", response_model=DashboardStats)
async def dashboard_stats(
    user: Annotated[User, Depends(require_role(UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    users = await db.scalar(select(func.count()).select_from(User))
    docs = await db.scalar(select(func.count()).select_from(Document))
    indexed = await db.scalar(
        select(func.count()).select_from(Document).where(Document.status == "indexed")
    )
    evals = await db.scalar(select(func.count()).select_from(EvaluationRun))
    return DashboardStats(
        total_users=users or 0,
        total_documents=docs or 0,
        indexed_documents=indexed or 0,
        total_evaluations=evals or 0,
    )


@router.get("/audit-logs")
async def audit_logs(
    user: Annotated[User, Depends(require_role(UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = 50,
):
    result = await db.execute(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit))
    return [
        {
            "id": str(log.id),
            "action": log.action,
            "resource": log.resource,
            "details": log.details,
            "created_at": log.created_at.isoformat(),
        }
        for log in result.scalars().all()
    ]


@router.post("/evaluate")
async def trigger_evaluation(
    payload: EvalRequest,
    user: Annotated[User, Depends(require_role(UserRole.ADMIN, UserRole.ANALYST))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    metrics = await run_evaluation(payload.dataset_name)
    run = EvaluationRun(dataset_name=payload.dataset_name, metrics=metrics, created_by=user.id)
    db.add(run)
    db.add(AuditLog(user_id=user.id, action="evaluation_run", resource=payload.dataset_name, details=metrics))
    await db.commit()
    return {"dataset": payload.dataset_name, "metrics": metrics}
