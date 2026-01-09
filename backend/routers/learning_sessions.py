from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from backend.database import SessionDep
from backend.dependencies.dependency import CurrentUser
from backend.models.learn_session import LearningSession, LearningSessionRead, LearningSessionStart, LearningSessionStop

router = APIRouter(prefix="/learning-sessions", tags=["learning-sessions"])


@router.post("/start", response_model=LearningSessionRead, status_code=201)
def start_session(payload: LearningSessionStart, session: SessionDep, current_user: CurrentUser):
    active = session.exec(
        select(LearningSession)
        .where(LearningSession.user_id == current_user.id)
        .where(LearningSession.ended_at.is_(None))
    ).first()
    if active:
        raise HTTPException(status_code=409, detail="A session is already active")

    ls = LearningSession(
        user_id=current_user.id,
        subject_id=payload.subject_id,
        started_at=datetime.now(timezone.utc),
        ended_at=None,
    )
    session.add(ls)
    session.commit()
    session.refresh(ls)
    return ls


@router.post("/{session_id}/stop", response_model=LearningSessionRead)
def stop_session(session_id: int, payload: LearningSessionStop, session: SessionDep, current_user: CurrentUser):
    ls = session.get(LearningSession, session_id)
    if not ls or ls.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")

    if ls.ended_at is not None:
        raise HTTPException(status_code=409, detail="Session already stopped")

    ls.ended_at = payload.ended_at or datetime.now(timezone.utc)
    if ls.ended_at <= ls.started_at:
        raise HTTPException(status_code=400, detail="ended_at must be after started_at")

    session.add(ls)
    session.commit()
    session.refresh(ls)
    return ls


@router.get("/active", response_model=LearningSessionRead | None)
def get_active_session(session: SessionDep, current_user: CurrentUser):
    return session.exec(
        select(LearningSession)
        .where(LearningSession.user_id == current_user.id)
        .where(LearningSession.ended_at.is_(None))
    ).first()