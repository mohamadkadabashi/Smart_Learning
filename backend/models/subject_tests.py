from datetime import datetime, timezone
from typing import Optional, Annotated
from pydantic import StringConstraints
from sqlmodel import SQLModel, Field
from sqlalchemy import CheckConstraint

class SubjectTestBase(SQLModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(nullable=False)

class SubjectTest(SubjectTestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Gibt es eine Möglichkeit das direkt als XML abzuspeichern?
    test: Optional[str] = None  # XML-Inhalt als TEXT
    question_type: Optional[str] = None
    subject_id: int = Field(foreign_key="subject.id", nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class SubjectTestCreate(SubjectTestBase):
    # Potenziell mehr Daten, je nachdem was für Erstellung in n8n gebraucht wird
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
    question_type: Optional[str] = Field(nullable=False)

class SubjectTestRead(SubjectTestBase):
    id: int
    # Gibt es eine Möglichkeit das direkt als XML abzuspeichern?
    test: str
    question_type: str
    subject_id: int
    created_at: datetime
    updated_at: datetime
