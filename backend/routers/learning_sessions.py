from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from dependencies.dependency import CurrentUser
from db.database import SessionDep

from models.learning_session import LearningSession, LearningSessionRead, LearningSessionStart, LearningSessionStop
from config.logger_config import logger


router = APIRouter(prefix="/learning-sessions", tags=["learning-sessions"])


@router.post("/start", response_model=LearningSessionRead, status_code=201)
def start_session(payload: LearningSessionStart, session: SessionDep, current_user: CurrentUser):
    active = session.exec(
        select(LearningSession)
        .where(LearningSession.user_id == current_user.id)
        .where(LearningSession.ended_at.is_(None))
    ).first()
    if active:
        logger.error(f"User {current_user.id} already has an active session")
        raise HTTPException(status_code=409, detail="A session is already active")

    ls = LearningSession(
        user_id=current_user.id,
        subject_id=payload.subject_id,
        started_at=datetime.now(timezone.utc),
        ended_at=None,
    )

    logger.info(f"Session {ls.id} started for user {current_user.id} and subject {payload.subject_id}")
    session.add(ls)
    session.commit()
    session.refresh(ls)
    return ls


@router.post("/{session_id}/stop", response_model=LearningSessionRead)
def stop_session(session_id: int, payload: LearningSessionStop, session: SessionDep, current_user: CurrentUser):
    ls = session.get(LearningSession, session_id)
    if not ls or ls.user_id != current_user.id:
        logger.error(f"Session {session_id} not found or not owned by user {current_user.id}")
        raise HTTPException(status_code=404, detail="Session not found")

    if ls.ended_at is not None:
        logger.error(f"Session {session_id} already stopped")
        raise HTTPException(status_code=409, detail="Session already stopped")

    end = payload.ended_at or datetime.now(timezone.utc)
    if end <= ls.started_at:
        logger.error(f"ended_at must be after started_at")
        raise HTTPException(status_code=400, detail="ended_at must be after started_at")

    logger.info(f"Session {session_id} stopped")
    ls.ended_at = end
    session.add(ls)
    session.commit()
    session.refresh(ls)
    return ls