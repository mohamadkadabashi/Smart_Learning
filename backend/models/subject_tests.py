from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Literal, Optional, Annotated
from pydantic import StringConstraints
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import CheckConstraint
from enum import Enum
from fastapi import Form

from models.attempt_tests import AttemptStatus

class SubjectTestStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"

class SubjectTestQuestionType(str, Enum):
    SINGLE_CHOICE  = "Single Choice"
    MULTIPLE_CHOICE = "Multiple Choice"
    GAP_TEXT = "Gap Text"

if TYPE_CHECKING:
    from models.subject import Subject
    from models.attempt_tests import TestAttempt

class SubjectTestBase(SQLModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(nullable=False)

class SubjectTest(SubjectTestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    test: Optional[str] = Field(default=None)  # XML TEXT

    # Request-metadata
    question_type: SubjectTestQuestionType = Field(default=SubjectTestQuestionType.SINGLE_CHOICE, nullable=False)
    question_count: int = Field(nullable=False)

    subject_id: int = Field(foreign_key="subject.id", nullable=False)

    # Async-Tracking
    status: SubjectTestStatus = Field(default=SubjectTestStatus.PENDING, nullable=False, index=True)
    job_id: Optional[str] = Field(default=None, index=True)     # correlation/execution id

    finished_at: Optional[datetime] = Field(default=None)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    subject: Optional["Subject"] = Relationship(back_populates="tests")

    attempts: List["TestAttempt"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    __table_args__ = (
        CheckConstraint("question_count>0", name="question_count_non_negative"),
    )

class SubjectTestCreate(SubjectTestBase):
    subject_id: int = Field(default=None, foreign_key="subject.id")
    #question_type: SubjectTestQuestionType = Field(default=SubjectTestQuestionType.SINGLE_CHOICE)
    question_count: int = Field(default=None)

    @classmethod
    def as_form(
        cls,
        name: Annotated[str, Form(...)],
        subject_id: Annotated[int, Form(...)],
        question_count: Annotated[int, Form(...)],
    ):
        return cls(
            name=name,
            subject_id=subject_id,
            question_count=question_count,
        )

class SubjectTestRead(SubjectTestBase):
    id: int
    test: Optional[str]
    question_type: SubjectTestQuestionType
    question_count: int
    subject_id: int

    status: SubjectTestStatus
    job_id: Optional[str]
    finished_at: Optional[datetime]

    created_at: datetime
    updated_at: datetime

class SubjectTestUpdate(SQLModel):
    name: Annotated[Optional[str], StringConstraints(strip_whitespace=True, min_length=1)] = None

class N8NCallbackPayload(SQLModel):
    xml: Optional[str] = None
    error: Optional[str] = None


class SubjectTestProgressRead(SQLModel):
    id: int
    subject_id: int
    name: str

    test_status: SubjectTestStatus  # PENDING/RUNNING/DONE/FAILED (n8n)

    attempt_status: Optional[AttemptStatus] = None  # in_progress/passed/failed/...
    correct_answered: Optional[int] = None
    total_questions: Optional[int] = None
    score_ratio: Optional[float] = None
    finished_at: Optional[datetime] = None

