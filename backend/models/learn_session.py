from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class LearningSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False
    )
    ended_at: Optional[datetime] = Field(default=None, index=True)

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