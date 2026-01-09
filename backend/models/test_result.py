from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class TestResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)
    subject_test_id: int = Field(
        foreign_key="subjecttest.id",
        index=True,
        nullable=False
    )

    # results
    correct_answered: int = Field(ge=0, nullable=False)
    total_questions: int = Field(ge=1, nullable=False)

    # Timestamp for stats
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False
    )

    duration_seconds: Optional[int] = Field(default=None, ge=0)
