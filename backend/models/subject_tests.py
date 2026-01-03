from datetime import datetime, timezone
from typing import Literal, Optional, Annotated
from pydantic import StringConstraints
from sqlmodel import SQLModel, Field
from sqlalchemy import CheckConstraint
from enum import Enum

class SubjectTestStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"

class SubjectTestBase(SQLModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(nullable=False)

class SubjectTest(SubjectTestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    test: Optional[str] = Field(default=None)  # XML TEXT

    # Request-metadata
    question_type: Optional[str] = Field(default=None)
    question_count: int = Field(nullable=False)
    subject_id: int = Field(foreign_key="subject.id", nullable=False)

    # Async-Tracking
    status: SubjectTestStatus = Field(default=SubjectTestStatus.PENDING, nullable=False, index=True)
    job_id: Optional[str] = Field(default=None, index=True)     # correlation/execution id
    error_message: Optional[str] = Field(default=None)

    finished_at: Optional[datetime] = Field(default=None)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("question_count>0", name="question_count_non_negative"),
    )

class SubjectTestCreate(SubjectTestBase):
    subject_id: int = Field(default=None, foreign_key="subject.id")
    question_type: str = Field(default=None)
    question_count: int = Field(default=None)

class SubjectTestRead(SubjectTestBase):
    id: int
    test: Optional[str]
    question_type: Optional[str]
    question_count: int
    subject_id: int

    status: SubjectTestStatus
    job_id: Optional[str]
    error_message: Optional[str]
    finished_at: Optional[datetime]

    created_at: datetime
    updated_at: datetime

class SubjectTestUpdate(SQLModel):
    name: Annotated[Optional[str], StringConstraints(strip_whitespace=True, min_length=1)] = None

class N8NCallbackPayload(SQLModel):
    xml: Optional[str] = None
    error: Optional[str] = None
