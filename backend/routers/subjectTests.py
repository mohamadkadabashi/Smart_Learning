from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database import SessionDep
from models.subjectTests import (
    SubjectTests,
    SubjectTestsCreate,
    SubjectTestsRead,
    SubjectTestsUpdate,
)

router = APIRouter(prefix="/subjectTests", tags=["subjectTests"])


@router.post("/", response_model=SubjectTestsRead, status_code=201)
def create_subject_test(
    subject_test_create: SubjectTestsCreate,
    session: SessionDep
):
    db_subject_test = SubjectTests.from_orm(subject_test_create)
    session.add(db_subject_test)
    session.commit()
    session.refresh(db_subject_test)
    return db_subject_test


@router.get("/", response_model=List[SubjectTestsRead])
def read_subject_tests(
    session: SessionDep
):
    subject_tests = session.exec(select(SubjectTests)).all()
    return subject_tests


@router.get("/bySubject/{subject_id}", response_model=List[SubjectTestsRead])
def read_subject_tests_of_subject(
    subject_id: int,
    session: SessionDep
):
    subject_tests = session.exec(select(SubjectTests).where(SubjectTests.subject_id == subject_id)).all()
    return subject_tests


@router.get("/{subject_test_id}", response_model=SubjectTestsRead)
def get_subject_test(
    subject_test_id: int,
    session: SessionDep
):
    subject_test = session.get(SubjectTests, subject_test_id)
    if not subject_test:
        raise HTTPException(status_code=404, detail="Subject test not found")
    return subject_test


@router.patch("/{subject_test_id}", response_model=SubjectTestsRead)
def update_subject_test(
    subject_test_id: int,
    subject_test_update: SubjectTestsUpdate,
    session: SessionDep
):
    subject_test = session.get(SubjectTests, subject_test_id)
    if not subject_test:
        raise HTTPException(status_code=404, detail="Subject test not found")
    
    update_data = subject_test_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subject_test, key, value)

    session.add(subject_test)
    session.commit()
    session.refresh(subject_test)
    return subject_test


@router.delete("/{subject_test_id}", status_code=204)
def delete_subject_test(
    subject_test_id: int,
    session: SessionDep
):
    subject_test = session.get(SubjectTests, subject_test_id)
    if not subject_test:
        raise HTTPException(status_code=404, detail="Subject test not found")

    session.delete(subject_test)
    session.commit()
