from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.testResult import TestResult, TestResultCreate, TestResultRead

router = APIRouter(prefix="/testresults", tags=["testresults"])


@router.get("/", response_model=list[TestResultRead])
def get_testresults(session: Session = Depends(get_session)):
    results = session.exec(select(TestResult)).all()
    return results


@router.get("/{resultid}", response_model=TestResultRead)
def get_testresult(resultid: int, session: Session = Depends(get_session)):
    result = session.get(TestResult, resultid)
    if not result:
        raise HTTPException(status_code=404, detail="TestResult not found")
    return result


@router.get("/byUser/{userid}", response_model=list[TestResultRead])
def get_testresults_by_user(userid: int, session: Session = Depends(get_session)):
    results = session.exec(select(TestResult).where(TestResult.userid == userid)).all()
    return results


@router.post("/", response_model=TestResultRead)
def create_testresult(result: TestResultCreate, session: Session = Depends(get_session)):
    new_result = TestResult.from_orm(result)
    session.add(new_result)
    session.commit()
    session.refresh(new_result)
    return new_result


@router.delete("/{resultid}")
def delete_testresult(resultid: int, session: Session = Depends(get_session)):
    result = session.get(TestResult, resultid)
    if not result:
        raise HTTPException(status_code=404, detail="TestResult not found")
    session.delete(result)
    session.commit()
    return {"status": "deleted"}
