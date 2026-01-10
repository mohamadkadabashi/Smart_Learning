from datetime import datetime, timezone
from typing import Literal, Optional
from sqlmodel import Column, DateTime, SQLModel, Field
from enum import Enum

class AttemptStatus(str, Enum):
    in_progress = "in_progress"
    passed = "passed"
    failed = "failed"
    abandoned = "abandoned"


class TestAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)
    subject_test_id: int = Field(foreign_key="subjecttest.id", index=True, nullable=False)

    status: AttemptStatus = Field(default=AttemptStatus.in_progress, index=True, nullable=False)

    # Timing (timestamptz in Postgres)
    started_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, index=True),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    finished_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True, index=True),
        default=None,
    )

    correct_answered: Optional[int] = Field(default=None, ge=0)
    total_questions: Optional[int] = Field(default=None, ge=1)
    score_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0)

    resumed_from_attempt_id: Optional[int] = Field(default=None, foreign_key="testattempt.id", index=True)
    
    progress_json: Optional[str] = Field(default=None)


class AttemptStart(SQLModel):
    subject_test_id: int
    resumed_from_attempt_id: Optional[int] = None
    progress_json: Optional[str] = None

class AttemptProgressUpdate(SQLModel):
    progress_json: str

class AttemptFinish(SQLModel):
    status: Literal["passed", "failed", "abandoned"]
    correct_answered: Optional[int] = None
    total_questions: Optional[int] = None
    finished_at: Optional[datetime] = None

class AttemptRead(SQLModel):
    id: int
    user_id: int
    subject_test_id: int
    status: str
    started_at: datetime
    updated_at: datetime
    finished_at: Optional[datetime]
    correct_answered: Optional[int]
    total_questions: Optional[int]
    score_ratio: Optional[float]
    progress_json: Optional[str]
    resumed_from_attempt_id: Optional[int]


class StatsOverview(SQLModel):
    study_time_week_seconds: int
    study_time_prev_week_seconds: int
    pass_rate_week: float
    tests_passed_week: int
    tests_total_week: int
    tests_done_today: int
    tests_remaining_today: int
