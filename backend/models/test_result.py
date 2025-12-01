from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class TestResultBase(SQLModel):
    user_id: int = Field(foreign_key="user.id", nullable=False)
    subject_test_id: int = Field(foreign_key="subjecttest.id", nullable=False)
    correct_answered: int
    total_questions: int


class TestResult(TestResultBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
