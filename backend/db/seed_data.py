from datetime import datetime, timezone, timedelta
from sqlmodel import Session, select

from models.user import User
from models.subject import Subject
from models.subject_tests import SubjectTest, SubjectTestQuestionType
from models.attempt_tests import TestAttempt, AttemptStatus
from models.learning_session import LearningSession
from config.auth import hash_password


subject_test1= """
<?xml version="1.0" encoding="UTF-8"?>
    <qti-assessment-item 
        xmlns="http://www.imsglobal.org/xsd/imsqtiasi_v3p0" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqtiasi_v3p0 https://www.imsglobal.org/xsd/qti/qtiv3p0/imsqti_asiv3p0_v1p0.xsd" 
        identifier="id_52b9f6f1-66bc-441c-b85a-e92923cff567" 
        title="Amortisierte Analyse von Hashing" 
        adaptive="false" 
        time-dependent="false">

        <qti-response-declaration identifier="RESPONSE_1" cardinality="single" base-type="identifier">
            <qti-correct-response>
                <qti-value>ID_1</qti-value>
            </qti-correct-response>
        </qti-response-declaration>

        <qti-outcome-declaration identifier="SCORE" cardinality="single" base-type="float">
            <qti-default-value>
                <qti-value>0.0</qti-value>
            </qti-default-value>
        </qti-outcome-declaration>

        <qti-outcome-declaration identifier="MAXSCORE" cardinality="single" base-type="float">
            <qti-default-value>
                <qti-value>1.0</qti-value>
            </qti-default-value>
        </qti-outcome-declaration>

        <qti-outcome-declaration identifier="FEEDBACKBASIC" cardinality="single" base-type="identifier">
            <qti-default-value>
                <qti-value>empty</qti-value>
            </qti-default-value>
        </qti-outcome-declaration>
    
        <qti-item-body>
            <p>Bei der dynamischen Größenänderung einer Hashtabelle wird der Belegungsfaktor β kontrolliert, um eine konstante mittlere Suchzeit zu gewährleisten. Dabei wird die Hashtabelle verdoppelt, sobald β &gt; 1 erreicht wird, und halbiert, wenn β &lt; 1/2. Welche der folgenden Aussagen beschreibt korrekt die Grundidee der amortisierten Analyse im Kontext der Löschoperationen in einer Hashtabelle, wenn der Schwellwert für die Verkleinerung β = 1/2 beträgt? (Quelle: Seite 7 / Kapitel 2.3)</p>
            <qti-choice-interaction response-identifier="RESPONSE_1" shuffle="true" max-choices="1">
                
                    <qti-simple-choice identifier="ID_1">
                        <p>Die Kosten für das Umspeichern der Elemente bei einer Tabellenverkleinerung werden auf die vorhergehenden Löschoperationen verteilt, sodass jede Löschoperation im Durchschnitt amortisiert in O(1) liegt.</p>
                    </qti-simple-choice>
                    <qti-simple-choice identifier="ID_2">
                        <p>Da die Tabellenverkleinerung nur bei einer sehr geringen Anzahl von Elementen erfolgt, ist die Worst-Case-Laufzeit einer Löschoperation immer O(1).</p>
                    </qti-simple-choice>
                    <qti-simple-choice identifier="ID_3">
                        <p>Die amortisierten Kosten einer Löschoperation sind nur dann O(1), wenn die Hashtabelle vorher durch eine Vergrößerung stabilisiert wurde.</p>
                    </qti-simple-choice>
                    <qti-simple-choice identifier="ID_4">
                        <p>Die amortisierten Kosten einer Löschoperation sind O(log n), da die Verkleinerung der Tabelle rekursiv durchgeführt wird.</p>
                    </qti-simple-choice>
            </qti-choice-interaction>
        </qti-item-body>

        <qti-response-processing>
            <qti-response-condition>
                <qti-response-if>
                    <qti-is-null>
                        <qti-variable identifier="RESPONSE_1"/>
                    </qti-is-null>
                </qti-response-if>
                <qti-response-else-if>
                    <qti-match>
                        <qti-variable identifier="RESPONSE_1"/>
                        <qti-correct identifier="RESPONSE_1"/>
                    </qti-match>
                    <qti-set-outcome-value identifier="SCORE">
                        <qti-sum>
                            <qti-variable identifier="SCORE"/>
                            <qti-variable identifier="MAXSCORE"/>
                        </qti-sum>
                    </qti-set-outcome-value>
                </qti-response-else-if>
            </qti-response-condition>
        </qti-response-processing>
    </qti-assessment-item>
"""

subject_test2="""
<?xml version="1.0" encoding="UTF-8"?>
    <qti-assessment-item 
        xmlns="http://www.imsglobal.org/xsd/imsqtiasi_v3p0" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqtiasi_v3p0 https://www.imsglobal.org/xsd/qti/qtiv3p0/imsqti_asiv3p0_v1p0.xsd" 
        identifier="id_d7083f5e-1c2d-4081-9108-8f0129725ea2" 
        title="Amortisierte Analyse" 
        adaptive="false" 
        time-dependent="false">

        <qti-response-declaration identifier="RESPONSE_1" cardinality="single" base-type="identifier">
            <qti-correct-response>
                <qti-value>ID_1</qti-value>
            </qti-correct-response>
        </qti-response-declaration>

        <qti-outcome-declaration identifier="SCORE" cardinality="single" base-type="float">
            <qti-default-value>
                <qti-value>0.0</qti-value>
            </qti-default-value>
        </qti-outcome-declaration>

        <qti-outcome-declaration identifier="MAXSCORE" cardinality="single" base-type="float">
            <qti-default-value>
                <qti-value>1.0</qti-value>
            </qti-default-value>
        </qti-outcome-declaration>

        <qti-outcome-declaration identifier="FEEDBACKBASIC" cardinality="single" base-type="identifier">
            <qti-default-value>
                <qti-value>empty</qti-value>
            </qti-default-value>
        </qti-outcome-declaration>
    
        <qti-item-body>
            <p>Welche Aussage trifft auf die amortisierte Analyse von Hash-Tabellen mit dynamischer Größenänderung zu, insbesondere im Kontext der Einfügeoperationen, wenn der Belegungsfaktor β = 1 als Schwellwert für die Verdopplung der Tabellengröße verwendet wird? (Quelle: Seite 7 / Kapitel 2.3)</p>
            <qti-choice-interaction response-identifier="RESPONSE_1" shuffle="true" max-choices="1">
                
                    <qti-simple-choice identifier="ID_1">
                        <p>Die amortisierten Kosten jeder Einfügeoperation liegen in O(1), da der Aufwand für die Tabellengrößeänderung auf alle vorherigen Einfügeoperationen verteilt wird.</p>
                    </qti-simple-choice>
                    <qti-simple-choice identifier="ID_2">
                        <p>Die amortisierten Kosten jeder Einfügeoperation liegen in O(n), da die Tabellengröße bei jedem Einfügen neu berechnet werden muss.</p>
                    </qti-simple-choice>
                    <qti-simple-choice identifier="ID_3">
                        <p>Die amortisierten Kosten liegen in O(log n), da die Hashfunktion mit steigender Tabellengröße komplexer wird.</p>
                    </qti-simple-choice>
                    <qti-simple-choice identifier="ID_4">
                        <p>Die amortisierten Kosten sind unabhängig von der Tabellengröße und betragen stets O(1), unabhängig von der Anzahl der Einfügeoperationen.</p>
                    </qti-simple-choice>
            </qti-choice-interaction>
        </qti-item-body>

        <qti-response-processing>
            <qti-response-condition>
                <qti-response-if>
                    <qti-is-null>
                        <qti-variable identifier="RESPONSE_1"/>
                    </qti-is-null>
                </qti-response-if>
                <qti-response-else-if>
                    <qti-match>
                        <qti-variable identifier="RESPONSE_1"/>
                        <qti-correct identifier="RESPONSE_1"/>
                    </qti-match>
                    <qti-set-outcome-value identifier="SCORE">
                        <qti-sum>
                            <qti-variable identifier="SCORE"/>
                            <qti-variable identifier="MAXSCORE"/>
                        </qti-sum>
                    </qti-set-outcome-value>
                </qti-response-else-if>
            </qti-response-condition>
        </qti-response-processing>
    </qti-assessment-item>
"""

def seed_database(session: Session) -> None:
    """
    Seeds demo data once (idempotent-ish):
    - creates demo user if not exists
    - creates subjects/tests/attempts/sessions if user has no subjects yet
    """

    now = datetime.now(timezone.utc)

   # Seed when user.id = 1 doesn't exist
    if session.get(User, 1) is not None:
        return

    # --------------------
    # 1) USER (id = 1)
    # --------------------
    demo_username = "demo_user"
    demo_email = "demo@example.com"
    demo_password_plain = "demo12345"

    # if user with username/email exists but not with id = 1 
    # then don't seed
    existing_by_name = session.exec(select(User).where(User.username == demo_username)).first()
    if existing_by_name is not None:
        return

    user = User(
        id=1,
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

    st1 = SubjectTest(
        subject_id=subj_math.id,
        name = "Mathe Test 1",
        test=subject_test2,
        question_type=SubjectTestQuestionType.MULTIPLE_CHOICE,
        question_count = 3,
        created_at=now,
        updated_at=now,
    )
    st2 = SubjectTest(
        subject_id=subj_math.id,
        name = "Mathe Test 2",
        test=subject_test1,
        question_type=SubjectTestQuestionType.MULTIPLE_CHOICE,
        question_count = 2,
        created_at=now,
        updated_at=now,
    )
    st3 = SubjectTest(
        subject_id=subj_physics.id,
        name = "Physik Test 1",
        test=subject_test1,
        question_type=SubjectTestQuestionType.SINGLE_CHOICE,
        question_count = 1,
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
