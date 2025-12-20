from fastapi import APIRouter, HTTPException, Depends
from models.subject_tests import SubjectTest, SubjectTestCreate, SubjectTestRead, SubjectTestUpdate
from models.subject import Subject
from database import SessionDep
from typing import List, Annotated
from sqlmodel import select
from config.logger_config import logger
from datetime import datetime, timezone
from dependencies.dependency import CurrentUser
from fastapi.security import OAuth2PasswordBearer
import requests
from pathlib import Path

router = APIRouter(prefix="/subjecttests", tags=["subjecttests"])
# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

@router.post("/", response_model=SubjectTestRead, status_code=201)
def create_subjectTest(
    subjectTest_create: SubjectTestCreate,
    session: SessionDep,
    current_user: CurrentUser,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    if not subjectTest_create.question_count > 0:
        logger.warning(f"Number of questions needs to be larger then 0 ({subjectTest_create.question_count})")
        raise HTTPException(status_code=400, detail="Number of questions needs to be larger then 0")
    
    subjects = session.exec(select(Subject).where(Subject.id == subjectTest_create.subject_id)).first()
    if not subjects:
        logger.warning(f"Subject {subjectTest_create.subject_id} does not exist, so no subjectTest creatable")
        raise HTTPException(status_code=404, detail="Subject not found")

    # Test von n8n anfordern
    webhook_url = "https://n8n.rattenserver.duckdns.org/webhook-test/d0575add-b533-4d10-9069-250f79d935c0"
    header = {"Authorization": f"Bearer {token}",
              "Accept": "application/json",}
    
    data = {
        "Thema": subjects.name,
        "Fragentyp": subjectTest_create.question_type,                            
        "question_count": str(subjectTest_create.question_count),
    }

    # TODO: File durch Nutzer auswählbar programmieren
    #file = open("BDP_01_NoSQL_Einfuehrung.pdf", "rb")
    scriptPath = Path(__file__).parent
    filePath = scriptPath / "BDP_01_NoSQL_Einfuehrung.pdf"
    #file = open(filePath, "rb")
    try:
        with open(filePath, "rb") as file:
            response = requests.post(
                url=webhook_url,
                headers=header,
                data=data,
                files={"file": (filePath.name, file, "application/pdf")},
                timeout=(30, 60),
            )
    except requests.exceptions.RequestException as err:
        logger.warning(err)
        raise HTTPException(status_code=408, detail="Failed to generate test")
        
    if response is None:
        logger.warning("No response object from n8n")
        raise HTTPException(status_code=502, detail="No response from n8n")

    if response.status_code >= 400:
        logger.warning(
            "n8n error status=%s body=%s",
            response.status_code,
            response.text[:1000],
        )
        raise HTTPException(status_code=502, detail=f"n8n returned {response.status_code}")
    
    if not response.text.strip().startswith("<?xml"):
        logger.warning("Response is not XML: %s", response.text[:200])

    # Test einspeisen
    # test = response.json()
    # response beinhaltet nur xml, also diese nicht erst als json ausgeben
    db_subjectTest = SubjectTest(
        name = subjectTest_create.name,
        # Ausgabe des Inhalts in response, sollte nur xml sein
        test = response.text,
        question_type = subjectTest_create.question_type,
        question_count = subjectTest_create.question_count,
        subject_id = subjectTest_create.subject_id
    )

    session.add(db_subjectTest)
    session.commit()
    session.refresh(db_subjectTest)
    logger.info(f"SubjectTest {db_subjectTest.name} (ID: {db_subjectTest.id}) for subject {db_subjectTest.subject_id} has been created")
    return db_subjectTest

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
