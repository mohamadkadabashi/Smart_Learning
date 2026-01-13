from fastapi import APIRouter, Body, HTTPException, Depends
from models.subject_tests import N8NCallbackPayload, SubjectTest, SubjectTestCreate, SubjectTestRead, SubjectTestUpdate, SubjectTestStatus
from models.subject import Subject
from db.database import SessionDep
from typing import List, Annotated
from sqlmodel import select
from config.logger_config import logger
from datetime import datetime, timezone
from dependencies.dependency import CurrentUser
from fastapi.security import OAuth2PasswordBearer
import uuid
import httpx
from pathlib import Path

router = APIRouter(prefix="/subjecttests", tags=["subjecttests"])
# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post("/", response_model=SubjectTestRead, status_code=202)
async def create_subjectTest(
    subjectTest_create: SubjectTestCreate,
    session: SessionDep,
    current_user: CurrentUser,
    token: Annotated[str, Depends(oauth2_scheme)],
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
        question_type=subjectTest_create.question_type,
        question_count=subjectTest_create.question_count,
        subject_id=subjectTest_create.subject_id,
        status=SubjectTestStatus.PENDING,
        job_id=job_id,
    )
    session.add(db_subjectTest)
    session.commit()
    session.refresh(db_subjectTest)

    # 2) trigger n8n
    webhook_url = "https://n8n.rattenserver.duckdns.org/webhook-test/d0575add-b533-4d10-9069-250f79d935c0"

    # Callback URL:
    callback_url = f"https://localhost:8000/subjecttest-callback/{job_id}"

    data = {
        "Thema": subject.name,
        "Fragentyp": subjectTest_create.question_type,
        "question_count": str(subjectTest_create.question_count),
        "job_id": job_id,
        "callback_url": callback_url,
    }

    scriptPath = Path(__file__).parent
    filePath = scriptPath / "BDP_01_NoSQL_Einfuehrung.pdf"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0)) as client:
            with open(filePath, "rb") as f:
                files = {"file": (filePath.name, f, "application/pdf")}
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
@router.post("/TEST", response_model = SubjectTestRead, status_code=201)
def PLACEHOLDERTESTcreate_subjectTest(
    subjectTest_create: SubjectTestCreate,
    session: SessionDep,
    current_user: CurrentUser
):
    db_subjectTest = SubjectTest(
        name = subjectTest_create.name,
        test = "test.xml",
        question_type = subjectTest_create.question_type,
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

@router.get("/bySubject/{subject_id}")
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
