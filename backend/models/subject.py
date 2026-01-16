from datetime import datetime, timezone
from typing import List, Optional, Annotated, TYPE_CHECKING
from pydantic import BaseModel, StringConstraints
from sqlmodel import Column, DateTime, Relationship, SQLModel, Field

if TYPE_CHECKING:
    from models.subject_tests import SubjectTest

# Model for subjects
class SubjectBase(SQLModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(nullable=False)

class Subject(SubjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    tests: List["SubjectTest"] = Relationship(
        back_populates="subject",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    
class SubjectCreate(SubjectBase):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class SubjectRead(SubjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class SubjectUpdate(SQLModel):
    name: Annotated[Optional[str], StringConstraints(strip_whitespace=True, min_length=1)] = None

class SubjectStats(SQLModel):
    subject_id: int
    subject_name: str
    tests_done: int

class SubjectProgressRead(BaseModel):
    id: int
    name: str
    total_tests: int
    passed_tests: int
