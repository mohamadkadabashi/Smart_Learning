from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TestResultBase(SQLModel):
    userid: int
    subjecttestid: int
    correctanswered: int
    totalquestions: int


class TestResult(TestResultBase, table=True):
    resultid: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TestResultRead(TestResultBase):
    resultid: int
    timestamp: datetime


class TestResultCreate(TestResultBase):
    pass
