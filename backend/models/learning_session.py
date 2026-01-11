from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Column, DateTime, SQLModel, Field


class LearningSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)

    started_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    ended_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True),
        default=None
    )

    # optional (wenn du später Auswertungen pro Fach willst)
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id", index=True)

class LearningSessionStart(SQLModel):
    subject_id: Optional[int] = None

class LearningSessionStop(SQLModel):
    ended_at: Optional[datetime] = None  # wenn None -> Server setzt now

class LearningSessionRead(SQLModel):
    id: int
    user_id: int
    started_at: datetime
    ended_at: Optional[datetime]
    subject_id: Optional[int]