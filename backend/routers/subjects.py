from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db.database import SessionDep
from config.logger_config import logger
from models.subject import Subject, SubjectCreate, SubjectRead, SubjectUpdate
from models.user import User

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("/", response_model=SubjectRead, status_code=201)
def create_subject(
    subject_create: SubjectCreate,
    session: SessionDep
):
    user_id_exists = session.exec(select(User).where(User.id == subject_create.user_id)).first()
    if not user_id_exists:
        logger.warning(f"User {subject_create.user_id} does not exist, no subject created")
        raise HTTPException(status_code=422, detail="User does not exist")
    
    subject_user_id_comb_exist = session.exec(select(Subject)
                                              .where(Subject.name == subject_create.name)
                                              .where(Subject.user_id == subject_create.user_id)).first()
    if subject_user_id_comb_exist:
        logger.warning(f"User {subject_create.user_id} already has subject with name {subject_create.name}")
        raise HTTPException(status_code=409, detail="User already has subject with this name")
    
    db_subject = Subject(
        name=subject_create.name,
        user_id=subject_create.user_id
    )

    session.add(db_subject)
    session.commit()
    session.refresh(db_subject)
    logger.info(f"Subject {db_subject.name} (ID: {db_subject.id}) for user-id {db_subject.user_id} has been created")
    return db_subject

@router.get("/", response_model=List[SubjectRead])
def read_subjects(
    session: SessionDep
):
    subjects = session.exec(select(Subject)).all()
    return subjects

@router.get("/byUser/{user_id}", response_model=List[SubjectRead])
def read_subjects_of_user(
    user_id: int,
    session: SessionDep
):
    subjects = session.exec(select(Subject).where(Subject.user_id == user_id)).all()
    if not subjects:
        logger.warning(f"User {user_id} does not exist, so no subjects found")
        raise HTTPException(status_code=404, detail="User not found")
    return subjects

@router.get("/{subject_id}", response_model=SubjectRead)
def get_subject(
    subject_id: int,
    session: SessionDep
):
    subject = session.get(Subject, subject_id)
    if not subject:
        logger.warning(f"Subject with ID {subject_id} does not exist")
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.patch("/{subject_id}", response_model=SubjectUpdate)
def update_subject(
    subject_id: int,
    subject_update: SubjectUpdate,
    session: SessionDep
):
    subject = session.get(Subject, subject_id)
    if not subject:
        logger.warning(f"Subject {subject_id} does not exist, so no update")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subject_name_user_id_combo_exists = session.exec(select(Subject)
                                                     .where(Subject.name == subject_update.name)
                                                     .where(Subject.user_id == subject.user_id)).first()
    if subject_name_user_id_combo_exists:
        logger.warning(f"User {subject.user_id} already has subject with name {subject_update.name}")
        raise HTTPException(status_code=409, detail="User already has subject with this name")
    
    subject.name = subject_update.name
    
    session.add(subject)
    session.commit()
    session.refresh(subject)
    logger.info(f"Subject {subject_id} has been updated")
    return subject

@router.delete("/{subject_id}", status_code=204)
def delete_subject(
    subject_id: int,
    session: SessionDep
):
    subject = session.get(Subject, subject_id)
    if not subject:
        logger.warning(f"Subject {subject_id} does not exist, so no delete")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    session.delete(subject)
    session.commit()
    logger.info(f"Subject {subject_id} has been deleted")
    return None
