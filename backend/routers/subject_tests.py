from fastapi import APIRouter, HTTPException
from models.subject_tests import SubjectTest, SubjectTestCreate, SubjectTestRead
from database import SessionDep
import requests
from pathlib import Path
from config.logger_config import logger

router = APIRouter(prefix="/subjecttests", tags=["subjecttests"])

@router.post("/", response_model=SubjectTestRead, status_code=201)
def create_subjectTest(
    subjectTest_create: SubjectTestCreate,
    session: SessionDep
):
    # Test von n8n anfordern
    webhook_url = "https://n8n.Forschungsding.com/start"
    header = {"Content-Type": "application/json"}
    data = {
        "question_type": subjectTest_create.question_type,
        "question_count": subjectTest_create.question_count
    }
    # TODO: File durch Nutzer auswählbar programmieren
    #file = open("BDP_01_NoSQL_Einfuehrung.pdf", "rb")
    scriptPath = Path(__file__).parent
    filePath = scriptPath / "BDP_01_NoSQL_Einfuehrung.pdf"
    file = open(filePath, "rb")
    # TODO: Auth einfügen, sobald auf Branch bereitgestellt
    try:
        response = requests.post(url=webhook_url,
                                headers=header,
                                json=data,
                                files={"file": file}) # auth= später
    except requests.exceptions.RequestException as err:
        logger.warning(err)
        raise HTTPException(status_code=408, detail="Failed to generate test")

    # Test einspeisen
    # test = response.json()
    # response beinhaltet nur xml, also diese nicht erst als json ausgeben
    db_subjectTest = SubjectTest(
        name = subjectTest_create.name,
        # Ausgabe des Inhalts in response, sollte nur xml sein
        test = response.content,
        question_type = subjectTest_create.question_type,
        question_count = subjectTest_create.question_type,
        subject_id = subjectTest_create.subject_id
    )

    session.add(db_subjectTest)
    session.commit()
    session.refresh(db_subjectTest)
    logger.info(f"SubjectTest {db_subjectTest.name} (ID: {db_subjectTest.id}) for subject {db_subjectTest.id} has been created")
    return db_subjectTest
