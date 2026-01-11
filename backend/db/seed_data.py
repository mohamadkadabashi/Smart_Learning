from datetime import datetime, timezone, timedelta
from sqlmodel import Session, select

from models.user import User
from models.subject import Subject
from models.subject_tests import SubjectTest
from models.attempt_tests import TestAttempt, AttemptStatus
from models.learning_session import LearningSession
from config.auth import hash_password


def seed_database(session: Session) -> None:
    """
    Seeds demo data once (idempotent-ish):
    - creates demo user if not exists
    - creates subjects/tests/attempts/sessions if user has no subjects yet
    """

    now = datetime.now(timezone.utc)

    # --------------------
    # 1) USER
    # --------------------
    demo_username = "demo_user"
    demo_email = "demo@example.com"
    demo_password_plain = "demo12345"  # >= 8 chars

    user = session.exec(select(User).where(User.username == demo_username)).first()
    if not user:
        user = User(
            username=demo_username,
            email=demo_email,
            password=hash_password(demo_password_plain),
            daily_goal=3,
            streak_enabled=True,
            created_at=now,
            updated_at=now,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    # --------------------
    # 2) GUARD: already seeded?
    # (if user already has subjects, we assume seed ran)
    # --------------------
    already_seeded = session.exec(select(Subject.id).where(Subject.user_id == user.id)).first()
    if already_seeded:
        return

    # --------------------
    # 3) SUBJECTS
    # --------------------
    subj_math = Subject(
        name="Mathematik",
        user_id=user.id,
        created_at=now,
        updated_at=now,
    )
    subj_physics = Subject(
        name="Physik",
        user_id=user.id,
        created_at=now,
        updated_at=now,
    )

    session.add_all([subj_math, subj_physics])
    session.commit()
    session.refresh(subj_math)
    session.refresh(subj_physics)

    # --------------------
    # 4) SUBJECT TESTS
    # (NOTE: make SubjectTest timestamps timezone-aware;
    #  update your model if you still use datetime.utcnow)
    # --------------------
    st1 = SubjectTest(
        subject_id=subj_math.id,
        test="<xml>Mathe Test 1</xml>",
        question_type="multiple_choice",
        created_at=now,
        updated_at=now,
    )
    st2 = SubjectTest(
        subject_id=subj_math.id,
        test="<xml>Mathe Test 2</xml>",
        question_type="multiple_choice",
        created_at=now,
        updated_at=now,
    )
    st3 = SubjectTest(
        subject_id=subj_physics.id,
        test="<xml>Physik Test 1</xml>",
        question_type="single_choice",
        created_at=now,
        updated_at=now,
    )

    session.add_all([st1, st2, st3])
    session.commit()
    session.refresh(st1)
    session.refresh(st2)
    session.refresh(st3)

    # --------------------
    # 5) TEST ATTEMPTS
    # today: 2 passed, 1 failed
    # this week: +2
    # last week: +1
    # plus: one in_progress with progress_json
    # --------------------
    attempts = [
        TestAttempt(
            user_id=user.id,
            subject_test_id=st1.id,
            status=AttemptStatus.passed,
            started_at=now - timedelta(minutes=40),
            finished_at=now - timedelta(minutes=35),
            updated_at=now - timedelta(minutes=35),
            correct_answered=8,
            total_questions=10,
            score_ratio=0.8,
            resumed_from_attempt_id=None,
            progress_json=None,
        ),
        TestAttempt(
            user_id=user.id,
            subject_test_id=st2.id,
            status=AttemptStatus.passed,
            started_at=now - timedelta(minutes=30),
            finished_at=now - timedelta(minutes=25),
            updated_at=now - timedelta(minutes=25),
            correct_answered=9,
            total_questions=10,
            score_ratio=0.9,
            resumed_from_attempt_id=None,
            progress_json=None,
        ),
        TestAttempt(
            user_id=user.id,
            subject_test_id=st3.id,
            status=AttemptStatus.failed,
            started_at=now - timedelta(minutes=20),
            finished_at=now - timedelta(minutes=15),
            updated_at=now - timedelta(minutes=15),
            correct_answered=4,
            total_questions=10,
            score_ratio=0.4,
            resumed_from_attempt_id=None,
            progress_json=None,
        ),
        # earlier this week
        TestAttempt(
            user_id=user.id,
            subject_test_id=st1.id,
            status=AttemptStatus.passed,
            started_at=now - timedelta(days=2, minutes=30),
            finished_at=now - timedelta(days=2),
            updated_at=now - timedelta(days=2),
            correct_answered=7,
            total_questions=10,
            score_ratio=0.7,
            resumed_from_attempt_id=None,
            progress_json=None,
        ),
        TestAttempt(
            user_id=user.id,
            subject_test_id=st2.id,
            status=AttemptStatus.failed,
            started_at=now - timedelta(days=3, minutes=20),
            finished_at=now - timedelta(days=3),
            updated_at=now - timedelta(days=3),
            correct_answered=5,
            total_questions=10,
            score_ratio=0.5,
            resumed_from_attempt_id=None,
            progress_json=None,
        ),
        # last week
        TestAttempt(
            user_id=user.id,
            subject_test_id=st1.id,
            status=AttemptStatus.passed,
            started_at=now - timedelta(days=8, minutes=25),
            finished_at=now - timedelta(days=8),
            updated_at=now - timedelta(days=8),
            correct_answered=6,
            total_questions=10,
            score_ratio=0.6,
            resumed_from_attempt_id=None,
            progress_json=None,
        ),
        # in_progress to test resume
        TestAttempt(
            user_id=user.id,
            subject_test_id=st3.id,
            status=AttemptStatus.in_progress,
            started_at=now - timedelta(minutes=10),
            finished_at=None,
            updated_at=now - timedelta(minutes=1),
            correct_answered=None,
            total_questions=None,
            score_ratio=None,
            resumed_from_attempt_id=None,
            progress_json='{"currentIndex": 5, "answers": {"1":"A","2":"C"}}',
        ),
    ]
    session.add_all(attempts)
    session.commit()

    # --------------------
    # 6) LEARNING SESSIONS
    # this week: ~1h + 30min
    # last week: ~2h + 2h
    # --------------------
    learning_sessions = [
        # this week
        LearningSession(
            user_id=user.id,
            subject_id=subj_math.id,
            started_at=now - timedelta(hours=5),
            ended_at=now - timedelta(hours=4),
        ),
        LearningSession(
            user_id=user.id,
            subject_id=subj_physics.id,
            started_at=now - timedelta(hours=2),
            ended_at=now - timedelta(hours=1, minutes=30),
        ),
        # last week
        LearningSession(
            user_id=user.id,
            subject_id=subj_math.id,
            started_at=now - timedelta(days=8, hours=3),
            ended_at=now - timedelta(days=8, hours=1),
        ),
        LearningSession(
            user_id=user.id,
            subject_id=subj_physics.id,
            started_at=now - timedelta(days=9, hours=4),
            ended_at=now - timedelta(days=9, hours=2),
        ),
    ]
    session.add_all(learning_sessions)
    session.commit()
