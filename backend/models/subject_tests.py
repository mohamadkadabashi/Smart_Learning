from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class SubjectTestBase(SQLModel):
    subject_id: int = Field(foreign_key="subject.id")
    test: Optional[str] = None  # Inhalt ist XML, wird intern als TEXT gespeichert
    question_type: Optional[str] = None


class SubjectTest(SubjectTestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
