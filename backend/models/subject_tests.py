from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class SubjectTestBase(SQLModel):
    test: Optional[str] = None  # XML-Inhalt als TEXT
    question_type: Optional[str] = None

class SubjectTest(SubjectTestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
