from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Column, DateTime, SQLModel, Field

class SubjectTestBase(SQLModel):
    test: Optional[str] = None  # XML-Inhalt als TEXT
    question_type: Optional[str] = None

class SubjectTest(SubjectTestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id", nullable=False)
    
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )