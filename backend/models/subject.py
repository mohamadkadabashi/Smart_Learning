from datetime import datetime, timezone
from typing import Optional, Annotated
from pydantic import StringConstraints
from sqlmodel import SQLModel, Field

# Model for subjects
class SubjectBase(SQLModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(nullable=False)

class Subject(SubjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class SubjectCreate(SubjectBase):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class SubjectRead(SubjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class SubjectUpdate(SQLModel):
    name: Annotated[Optional[str], StringConstraints(strip_whitespace=True, min_length=1)] = None
