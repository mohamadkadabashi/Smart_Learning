from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from models.attempt_tests import AttemptStatus, TestAttempt
from models.subject_tests import N8NCallbackPayload, SubjectTest, SubjectTestCreate, SubjectTestProgressRead, SubjectTestRead, SubjectTestUpdate, SubjectTestStatus, SubjectTestQuestionType
from models.subject import Subject
from db.database import SessionDep
from typing import List, Annotated
from sqlmodel import case, func, select
from config.logger_config import logger
from config.setting import settings
from datetime import datetime, timezone
from dependencies.dependency import CurrentUser
from fastapi.security import OAuth2PasswordBearer
import uuid
import httpx
from pathlib import Path

router = APIRouter(prefix="/subjecttests", tags=["subjecttests"])
# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post("/{questionTyp_select}", response_model=SubjectTestRead, status_code=202)
async def create_subjectTest(
    session: SessionDep,
    current_user: CurrentUser,
    questionTyp_select: SubjectTestQuestionType,
    token: Annotated[str, Depends(oauth2_scheme)],
    file: UploadFile = File(...),
    subjectTest_create: SubjectTestCreate = Depends(SubjectTestCreate.as_form),
):
    if subjectTest_create.question_count <= 0:
        raise HTTPException(status_code=400, detail="Number of questions needs to be larger then 0")

    subject = session.exec(select(Subject).where(Subject.id == subjectTest_create.subject_id)).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # 1) create Job (PENDING)
    job_id = str(uuid.uuid4())
    db_subjectTest = SubjectTest(
        name=subjectTest_create.name,
        test="",  # empty
        question_type=questionTyp_select,
        question_count=subjectTest_create.question_count,
        subject_id=subjectTest_create.subject_id,
        status=SubjectTestStatus.PENDING,
        job_id=job_id,
    )
    session.add(db_subjectTest)
    session.commit()
    session.refresh(db_subjectTest)

    # 2) trigger n8n
    webhook_url = settings.N8N_WEBHOOK_URL


    # Callback URL:
    callback_url = f"https://localhost:8000/subjecttest-callback/{job_id}"

    data = {
        "Thema": subject.name,
        "Fragentyp": questionTyp_select.value,
        "question_count": str(subjectTest_create.question_count),
        "job_id": job_id,
        "callback_url": callback_url,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0)) as client:
            files = {"file": (file.filename, file.file, "application/pdf")}
            resp = await client.post(webhook_url, headers=headers, data=data, files=files)
            resp.raise_for_status()
                

    except Exception as e:
        # if Trigger failed then:
        db_subjectTest.status = SubjectTestStatus.FAILED
        session.add(db_subjectTest)
        session.commit()
        raise HTTPException(status_code=502, detail="Failed to trigger n8n")
    
    return db_subjectTest

@router.post("/n8n/subjecttest-callback/{job_id}", status_code=204)
async def n8n_subjecttest_callback(
    job_id: str,
    session: SessionDep,
    payload: N8NCallbackPayload
):

    db_subjectTest = session.exec(select(SubjectTest).where(SubjectTest.job_id == job_id)).first()
    if not db_subjectTest:
        raise HTTPException(status_code=404, detail="Job not found")

    if "error" in payload and payload["error"]:
        db_subjectTest.status = "FAILED"
        db_subjectTest.error = str(payload["error"])
        db_subjectTest.finished_at = datetime.now(timezone.utc)
        session.add(db_subjectTest)
        session.commit()
        return

    xml = (payload.get("xml") or "").strip()
    if not xml:
        raise HTTPException(status_code=400, detail="Missing xml")

    # XML basic check
    if not (xml.startswith("<") or xml.startswith("<?xml")):
        raise HTTPException(status_code=400, detail="Invalid xml")

    db_subjectTest.test = xml
    db_subjectTest.status = "DONE"
    db_subjectTest.error = None
    db_subjectTest.finished_at = datetime.now(timezone.utc)

    session.add(db_subjectTest)
    session.commit()
    return

# Testfunktion, um Daten für andere API Anfragen einzufügen
@router.post("/TEST/{questionTyp_select}", response_model = SubjectTestRead, status_code=201)
def PLACEHOLDERTESTcreate_subjectTest(
    subjectTest_create: SubjectTestCreate,
    session: SessionDep,
    questionTyp_select: SubjectTestQuestionType,
    current_user: CurrentUser
):
    db_subjectTest = SubjectTest(
        name = subjectTest_create.name,
        test = "test.xml",
        question_type = questionTyp_select,
        question_count = subjectTest_create.question_count,
        subject_id = subjectTest_create.subject_id
    )

    session.add(db_subjectTest)
    session.commit()
    session.refresh(db_subjectTest)
    logger.info(f"SubjectTest {db_subjectTest.name} (ID: {db_subjectTest.id}) for subject {db_subjectTest.id} has been created")
    return db_subjectTest

@router.get("/", response_model=List[SubjectTestRead])
def read_subjectTests(
    session: SessionDep,
    current_user: CurrentUser
):
    subjectTests = session.exec(select(SubjectTest)).all()
    return subjectTests

@router.get("/{subjectTest_id}", response_model=SubjectTestRead)
def get_subjectTest(
    subjectTest_id: int,
    session: SessionDep,
    current_user: CurrentUser
):
    subjectTest = session.get(SubjectTest, subjectTest_id)
    if not subjectTest:
        logger.warning(f"SubjectTest with ID {subjectTest_id} does not exist")
        raise HTTPException(status_code=404, detail="SubjectTest not found")
    return subjectTest

@router.patch("/{subjectTest_id}", response_model=SubjectTestRead)
def update_subjectTest(
    subjectTest_id: int,
    subjectTest_update: SubjectTestUpdate,
    session: SessionDep,
    current_user: CurrentUser
):
    subjectTest = session.get(SubjectTest, subjectTest_id)
    if not subjectTest:
        logger.warning(f"SubjectTest {subjectTest_id} does not exist, so no update")
        raise HTTPException(status_code=404, detail="SubjectTest not found")
    
    if subjectTest_update.name == None:
        logger.warning(f"No name to update entered")
        raise HTTPException(status_code=400, detail="No Name has been entered")

    
    subjectTest_name_subject_id_combo_exists = session.exec(select(SubjectTest)
                                                            .where(SubjectTest.name == subjectTest_update.name)
                                                            .where(SubjectTest.subject_id == subjectTest.subject_id)).first()

    if subjectTest_name_subject_id_combo_exists:
        logger.warning(f"Subject {subjectTest.subject_id} already has subjectTest with name {subjectTest_update.name}")
        raise HTTPException(status_code=409, detail="Subject already has subjectTest with this name")
    
    subjectTest.name = subjectTest_update.name
    subjectTest.updated_at = datetime.now(timezone.utc)
    
    session.add(subjectTest)
    session.commit()
    session.refresh(subjectTest)
    logger.info(f"SubjectTest {subjectTest_id} has been updated")
    return subjectTest

@router.delete("/{subjectTest_id}", status_code=204)
def delete_subjectTest(
    subjectTest_id: int,
    session: SessionDep,
    current_user: CurrentUser
):
    subjectTest = session.get(SubjectTest, subjectTest_id)
    if not subjectTest:
        logger.warning(f"SubjectTest {subjectTest_id} does not exist, so no delete")
        raise HTTPException(status_code=404, detail="SubjectTest not found")
    
    session.delete(subjectTest)
    session.commit()
    logger.info(f"SubjectTest {subjectTest_id} has been deleted")
    return None

@router.get("/bySubjects/{subject_id}")
def read_subjectTests_of_subject(
    subject_id: int,
    session: SessionDep,
    current_user: CurrentUser
):
    subject = session.exec(select(Subject).where(Subject.id == subject_id)).first()
    if not subject:
        logger.warning(f"Subject {subject_id} does not exist, so no subjectTests found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subjectTests = session.exec(select(SubjectTest).where(SubjectTest.subject_id == subject_id)).all()
    return subjectTests

PASS_THRESHOLD = 0.6

@router.get("/bySubject/{subject_id}", response_model=list[SubjectTestProgressRead])
def read_tests_by_subject_with_progress(subject_id: int, session: SessionDep, current_user: CurrentUser):

    latest_attempt_subq = (
        select(
            TestAttempt.subject_test_id.label("st_id"),
            func.max(TestAttempt.updated_at).label("max_updated_at")
        )
        .where(TestAttempt.user_id == current_user.id)
        .group_by(TestAttempt.subject_test_id)
        .subquery()
    )

    # computed attempt status:
    # - wenn kein Attempt: NULL
    # - wenn Attempt noch nicht finished: in_progress
    # - wenn finished: passed/failed anhand score_ratio (>=0.6)
    computed_attempt_status = case(
        (TestAttempt.id.is_(None), None),
        (TestAttempt.finished_at.is_(None), AttemptStatus.in_progress),
        (TestAttempt.score_ratio >= PASS_THRESHOLD, AttemptStatus.passed),
        else_=AttemptStatus.failed,
    )

    stmt = (
        select(
            SubjectTest.id.label("id"),
            SubjectTest.subject_id.label("subject_id"),
            SubjectTest.name.label("name"),
            SubjectTest.status.label("test_status"),

            computed_attempt_status.label("attempt_status"),
            func.coalesce(TestAttempt.correct_answered, 0).label("correct_answered"),
            func.coalesce(TestAttempt.total_questions, SubjectTest.question_count).label("total_questions"),
            TestAttempt.score_ratio.label("score_ratio"),
            TestAttempt.finished_at.label("finished_at"),
        )
        .where(SubjectTest.subject_id == subject_id)
        .outerjoin(latest_attempt_subq, latest_attempt_subq.c.st_id == SubjectTest.id)
        .outerjoin(
            TestAttempt,
            (TestAttempt.subject_test_id == SubjectTest.id)
            & (TestAttempt.user_id == current_user.id)
            & (TestAttempt.updated_at == latest_attempt_subq.c.max_updated_at)
        )
    )

    rows = session.exec(stmt).all()

    return [
        SubjectTestProgressRead(
            id=r.id,
            subject_id=r.subject_id,
            name=r.name,
            test_status=r.test_status,
            attempt_status=r.attempt_status,
            correct_answered=r.correct_answered,
            total_questions=r.total_questions,
            score_ratio=r.score_ratio,
            finished_at=r.finished_at,
        )
        for r in rows
    ]