"""REST endpoints (stateless, so they work on serverless hosts such as Vercel)."""
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.auth import current_user
from app.crew import run_pipeline
from app.schemas import RunRequest, RunResponse

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/run", response_model=RunResponse, dependencies=[Depends(current_user)])
def run(req: RunRequest) -> RunResponse:
    try:
        result = run_pipeline(req.requirement, req.model, req.temperature)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Agent pipeline failed: {exc}") from exc
    return RunResponse(run_id=uuid4().hex[:8], created_at=datetime.now(timezone.utc).isoformat(),
                       requirement=req.requirement, **result)
