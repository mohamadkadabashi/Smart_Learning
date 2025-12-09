from fastapi import APIRouter, HTTPException
from models.subject_tests import SubjectTest, SubjectTestCreate, SubjectTestRead
from database import SessionDep
import requests
from config.logger_config import logger

router = APIRouter(prefix="/subjecttests", tags=["subjecttests"])

@router.post("/", response_model=SubjectTestRead, status_code=201)
def create_subjectTest(
    subjectTest_create: SubjectTestCreate,
    session: SessionDep
):
    # Test von n8n anfordern
    webhook_url = "https://n8n.Forschungsding.com/start"
    header = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "question_type": subjectTest_create.question_type
    }
    response = requests.post(webhook_url, headers=header, json=data)

    if not response.status_code == 200:
        logger.warning(f"n8n request failed")
        raise HTTPException(status_code=response.status_code, detail="Failed to generate test") 

    # Test einspeisen
    test = response.json()
    return test

    
    # db_subject = SubjectTest(
    #     name=subject_create.name,
    #     user_id=subject_create.user_id
    # )

    # session.add(db_subject)
    # session.commit()
    # session.refresh(db_subject)
    # logger.info(f"Subject {db_subject.name} (ID: {db_subject.id}) for user-id {db_subject.user_id} has been created")
    # return db_subject
