from datetime import datetime, timezone
from typing import Optional, Annotated
from pydantic import StringConstraints
from sqlmodel import SQLModel, Field

class SubjectTestBase(SQLModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(nullable=False)

class SubjectTest(SubjectTestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    test: Optional[str] = None  # XML-Inhalt als TEXT
    question_type: Optional[str] = None
    question_count: Optional[int] = Field(default=None)
    subject_id: int = Field(foreign_key="subject.id", nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class SubjectTestCreate(SubjectTestBase):
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
    question_type: Optional[str] = Field(default=None)
    question_count: Optional[int] = Field(default=None)

class SubjectTestRead(SubjectTestBase):
    id: int
    test: str
    question_type: str
    question_count: int
    subject_id: int
    created_at: datetime
    updated_at: datetime

class SubjectTestUpdate(SQLModel):
    name: Annotated[Optional[str], StringConstraints(strip_whitespace=True, min_length=1)] = None
