from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from db.database import SessionDep
from dependencies.dependency import CurrentUser
from models.learning_session import LearningSession
from models.subject import Subject, SubjectStats
from models.subject_tests import SubjectTest
from models.attempt_tests import AttemptStatus, TestAttempt, StatsOverview
from models.user import User
from config.logger_config import logger


router = APIRouter(prefix="/stats", tags=["stats"])

BERLIN = ZoneInfo("Europe/Berlin")

def berlin_day_bounds_utc(now_utc: datetime):
    now_berlin = now_utc.astimezone(BERLIN)
    start_berlin = now_berlin.replace(hour=0, minute=0, second=0, microsecond=0)
    end_berlin = start_berlin + timedelta(days=1)
    return start_berlin.astimezone(timezone.utc), end_berlin.astimezone(timezone.utc)


def berlin_week_start_utc(now_utc: datetime) -> datetime:
    now_berlin = now_utc.astimezone(BERLIN)
    monday = (now_berlin - timedelta(days=now_berlin.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return monday.astimezone(timezone.utc)


def overlap_seconds(a_start, a_end, b_start, b_end) -> int:
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    if end <= start:
        return 0
    return int((end - start).total_seconds())


@router.get("/overview", response_model=StatsOverview)
def overview(session: SessionDep, current_user: CurrentUser):
    now = datetime.now(timezone.utc)
    day_start_utc, day_end_utc = berlin_day_bounds_utc(now)
    week_start_utc = berlin_week_start_utc(now)
    prev_week_start_utc = week_start_utc - timedelta(days=7)

    user = session.get(User, current_user.id)
    if not user:
        logger.error(f"User {current_user.id} not found")
        raise HTTPException(status_code=401, detail="User not found")

    # ---------- Tests today ----------
    tests_done_today = session.exec(
        select(func.count(TestAttempt.id))
        .where(TestAttempt.user_id == current_user.id)
        .where(TestAttempt.finished_at.is_not(None))
        .where(TestAttempt.finished_at >= day_start_utc)
        .where(TestAttempt.finished_at < day_end_utc)
        .where(TestAttempt.status.in_([ AttemptStatus.passed, AttemptStatus.failed ]))
    ).first() or 0
    logger.info(f"User {current_user.id} has {tests_done_today} tests done today")

    daily_goal = int(user.daily_goal or 1)
    tests_remaining_today = max(0, daily_goal - int(tests_done_today))

    # ---------- Tests this week ----------
    tests_total_week = session.exec(
        select(func.count(TestAttempt.id))
        .where(TestAttempt.user_id == current_user.id)
        .where(TestAttempt.finished_at.is_not(None))
        .where(TestAttempt.finished_at >= week_start_utc)
        .where(TestAttempt.finished_at < now)
        .where(TestAttempt.status.in_([ AttemptStatus.passed, AttemptStatus.failed]))
    ).first() or 0
    logger.info(f"User {current_user.id} has {tests_total_week} tests done this week")

    tests_passed_week = session.exec(
        select(func.count(TestAttempt.id))
        .where(TestAttempt.user_id == current_user.id)
        .where(TestAttempt.finished_at.is_not(None))
        .where(TestAttempt.finished_at >= week_start_utc)
        .where(TestAttempt.finished_at < now)
        .where(TestAttempt.status == AttemptStatus.passed)
    ).first() or 0
    logger.info(f"User {current_user.id} has {tests_passed_week} tests passed this week")

    # if only user pass the test with passed of the total tests in the week.
    pass_rate_week = (float(tests_passed_week) / float(tests_total_week)) if tests_total_week else 0.0

    # ---------- Study time this week + prev week ----------
    sessions = session.exec(
        select(LearningSession.started_at, LearningSession.ended_at)
        .where(LearningSession.user_id == current_user.id)
        .where(LearningSession.started_at >= prev_week_start_utc)
    ).all()
    logger.info(f"User {current_user.id} has {len(sessions)} learning sessions this week")


    study_time_week_seconds = 0
    study_time_prev_week_seconds = 0

    for s_at, e_at in sessions:
        end = e_at or now
        study_time_prev_week_seconds += overlap_seconds(s_at, end, prev_week_start_utc, week_start_utc)
        study_time_week_seconds += overlap_seconds(s_at, end, week_start_utc, now)

    logger.info(f"User {current_user.id} has {study_time_week_seconds} seconds of study time this week and {study_time_prev_week_seconds} seconds of study time prev week")

    return StatsOverview(
        study_time_week_seconds=int(study_time_week_seconds),
        study_time_prev_week_seconds=int(study_time_prev_week_seconds),
        pass_rate_week=float(pass_rate_week),
        tests_passed_week=int(tests_passed_week),
        tests_total_week=int(tests_total_week),
        tests_done_today=int(tests_done_today),
        tests_remaining_today=int(tests_remaining_today),
    )