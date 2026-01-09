from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from fastapi import APIRouter
from sqlmodel import func, select

from backend.database import SessionDep
from backend.dependencies.dependency import CurrentUser
from backend.models.learn_session import LearningSession
from backend.models.subject import StatsOverview, Subject, SubjectStats
from backend.models.subject_tests import SubjectTest
from backend.models.test_result import TestResult
from backend.models.user import User

router = APIRouter(prefix="/stats", tags=["stats"])
BERLIN = ZoneInfo("Europe/Berlin")


def berlin_day_bounds_utc(now_utc: datetime):
    now_berlin = now_utc.astimezone(BERLIN)
    start_berlin = now_berlin.replace(hour=0, minute=0, second=0, microsecond=0)
    end_berlin = start_berlin + timedelta(days=1)
    return start_berlin.astimezone(timezone.utc), end_berlin.astimezone(timezone.utc), now_berlin.date()


def berlin_week_start_utc(now_utc: datetime):
    now_berlin = now_utc.astimezone(BERLIN)
    monday = (now_berlin - timedelta(days=now_berlin.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    return monday.astimezone(timezone.utc)


@router.get("/overview")
def overview(session: SessionDep, current_user: CurrentUser):
    now = datetime.now(timezone.utc)
    day_start_utc, day_end_utc, today_berlin = berlin_day_bounds_utc(now)
    week_start_utc = berlin_week_start_utc(now)

    user = session.get(User, current_user.id)

    # tests done today
    tests_done_today = session.exec(
        select(func.count(TestResult.id))
        .where(TestResult.user_id == current_user.id)
        .where(TestResult.timestamp >= day_start_utc)
        .where(TestResult.timestamp < day_end_utc)
    ).one() or 0

    remaining = max(0, (user.daily_goal or 1) - int(tests_done_today))

    # pass rate this week (sum correct / sum total)
    correct_sum, total_sum = session.exec(
        select(
            func.coalesce(func.sum(TestResult.correct_answered), 0),
            func.coalesce(func.sum(TestResult.total_questions), 0),
        )
        .where(TestResult.user_id == current_user.id)
        .where(TestResult.timestamp >= week_start_utc)
    ).one()
    pass_rate_week = float(correct_sum) / float(total_sum) if total_sum else 0.0

    # study time this week: sum(ended-started)
    sessions_rows = session.exec(
        select(LearningSession.started_at, LearningSession.ended_at)
        .where(LearningSession.user_id == current_user.id)
        .where(LearningSession.started_at >= week_start_utc)
    ).all()

    study_seconds = 0
    for s_at, e_at in sessions_rows:
        if e_at and e_at > s_at:
            study_seconds += int((e_at - s_at).total_seconds())

    # streak: count consecutive days with >= 1 TestResult (Berlin days)
    streak_days = 0
    if user.streak_enabled:
        # get unique berlin dates where user has at least one test
        # easiest approach: fetch timestamps and convert to berlin dates (ok for moderate data)
        # If huge dataset: do DB-side date conversion depending on DB.
        ts = session.exec(
            select(TestResult.timestamp)
            .where(TestResult.user_id == current_user.id)
            .order_by(TestResult.timestamp.desc())
            .limit(2000)
        ).all()

        dates = []
        seen = set()
        for t in ts:
            d = t.astimezone(BERLIN).date()
            if d not in seen:
                seen.add(d)
                dates.append(d)

        # compute streak starting from today_berlin
        expected = today_berlin
        s = set(dates)
        while expected in s:
            streak_days += 1
            expected = expected - timedelta(days=1)

    return {
        "tests_done_today": int(tests_done_today),
        "tests_remaining_today": int(remaining),
        "pass_rate_week": pass_rate_week,
        "study_time_week_seconds": int(study_seconds),
        "current_streak_days": int(streak_days),
    }


@router.get("/by-subject")
def by_subject(session: SessionDep, current_user: CurrentUser):
    rows = session.exec(
        select(
            Subject.id,
            Subject.name,
            func.count(TestResult.id),
        )
        .join(SubjectTest, SubjectTest.subject_id == Subject.id)
        .join(TestResult, TestResult.subject_test_id == SubjectTest.id)
        .where(TestResult.user_id == current_user.id)
        .group_by(Subject.id, Subject.name)
        .order_by(func.count(TestResult.id).desc())
    ).all()

    return [{"subject_id": sid, "subject_name": name, "tests_done": int(cnt)} for sid, name, cnt in rows]
