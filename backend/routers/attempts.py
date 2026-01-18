from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db.database import SessionDep
from dependencies.dependency import CurrentUser
from models.subject_tests import SubjectTest
from models.attempt_tests import AttemptFinish, AttemptProgressUpdate, AttemptRead, AttemptStart, AttemptStatus, TestAttempt
from config.logger_config import logger

router = APIRouter(prefix="/attempts", tags=["attempts"])

PASS_THRESHOLD = 0.6

@router.post("/start", response_model=AttemptRead, status_code=201)
def start_attempt(payload: AttemptStart, session: SessionDep, current_user: CurrentUser):
    st = session.get(SubjectTest, payload.subject_test_id)
    if not st:
        raise HTTPException(status_code=404, detail="SubjectTest not found")

    existing = session.exec(
        select(TestAttempt)
        .where(TestAttempt.user_id == current_user.id)
        .where(TestAttempt.subject_test_id == payload.subject_test_id)
        .where(TestAttempt.status == AttemptStatus.in_progress)
        .order_by(TestAttempt.updated_at.desc())
    ).first()

    # ✅ RESUME statt 409
    if existing:
        # optional: progress_json updaten, wenn du beim Start was mitschickst
        if payload.progress_json is not None:
            existing.progress_json = payload.progress_json
            existing.updated_at = datetime.now(timezone.utc)
            session.add(existing)
            session.commit()
            session.refresh(existing)

        return existing

    now = datetime.now(timezone.utc)
    attempt = TestAttempt(
        user_id=current_user.id,
        subject_test_id=payload.subject_test_id,
        status=AttemptStatus.in_progress,
        started_at=now,
        updated_at=now,
        finished_at=None,
        correct_answered=None,
        total_questions=None,
        score_ratio=None,
        progress_json=payload.progress_json,
        resumed_from_attempt_id=payload.resumed_from_attempt_id,
    )

    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    return attempt



@router.patch("/{attempt_id}/progress", response_model=AttemptRead)
def update_progress(attempt_id: int, payload: AttemptProgressUpdate, session: SessionDep, current_user: CurrentUser):
    attempt = session.get(TestAttempt, attempt_id)
    if not attempt or attempt.user_id != current_user.id:
        logger.error(f"Attempt {attempt_id} not found or not owned by user {current_user.id}")
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.status != AttemptStatus.in_progress:
        logger.error(f"Attempt {attempt_id} is not in_progress")
        raise HTTPException(status_code=409, detail="Only in_progress attempts can be updated")

    attempt.progress_json = payload.progress_json
    attempt.updated_at = datetime.now(timezone.utc)

    logger.info(f"Attempt {attempt_id} progress updated")
    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    return attempt

@router.post("/{attempt_id}/finish", response_model=AttemptRead)
def finish_attempt(attempt_id: int, payload: AttemptFinish, session: SessionDep, current_user: CurrentUser):
    attempt = session.get(TestAttempt, attempt_id)

    if not attempt or attempt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.status != AttemptStatus.in_progress:
        raise HTTPException(status_code=409, detail="Attempt already finished")

    # validate
    if payload.total_questions <= 0:
        raise HTTPException(status_code=400, detail="total_questions must be > 0")
    if payload.correct_answered < 0 or payload.correct_answered > payload.total_questions:
        raise HTTPException(status_code=400, detail="correct_answered must be between 0 and total_questions")

    now = datetime.now(timezone.utc)
    finished_at = payload.finished_at or now

    score_ratio = float(payload.correct_answered) / float(payload.total_questions)

    attempt.correct_answered = payload.correct_answered
    attempt.total_questions = payload.total_questions
    attempt.score_ratio = score_ratio

    # IMPORTANT: status computed here
    attempt.status = AttemptStatus.passed if score_ratio >= PASS_THRESHOLD else AttemptStatus.failed

    attempt.finished_at = finished_at
    attempt.updated_at = now

    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    return attempt
