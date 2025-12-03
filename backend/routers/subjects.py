from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.subject import Subject, SubjectCreate, SubjectRead, SubjectUpdate

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("/", response_model=SubjectRead, status_code=201)
def create_subject(
    subject_create: SubjectCreate,
    session: SessionDep
):
    name_exists = session.exec(select(Subject).where(Subject.name == subject_create.name)).first()
    user_id_exists = session.exec(select(Subject).where(Subject.user_id == subject_create.user_id)).first()
    if name_exists and user_id_exists:
        raise HTTPException(status_code=400, detail="User already has subject with this name")
    
    db_subject = Subject(
        name=subject_create.name,
        user_id=subject_create.user_id
    )

    session.add(db_subject)
    session.commit()
    session.refresh(db_subject)
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
        raise HTTPException(status_code=404, detail="User not found")
    return subjects

@router.get("/{subject_id}", response_model=SubjectRead)
def get_subject(
    subject_id: int,
    session: SessionDep
):
    subject = session.get(Subject, subject_id)
    if not subject:
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
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subject.name = subject_update.name
    
    session.add(subject)
    session.commit()
    session.refresh(subject)
    return subject

@router.delete("/{subject_id}", status_code=204)
def delete_subject(
    subject_id: int,
    session: SessionDep
):
    subject = session.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    session.delete(subject)
    session.commit()
    return None
