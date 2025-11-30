from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class SubjectTestsBase(SQLModel):
    subject_id: int = Field(foreign_key="subject.id", nullable=False)
    test: Optional[str] = Field(default=None)  # XML stored as text
    questiontyp: Optional[str] = Field(default=None)


class SubjectTests(SubjectTestsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class SubjectTestsCreate(SubjectTestsBase):
    pass


class SubjectTestsRead(SubjectTestsBase):
    id: int
    created_at: datetime
    updated_at: datetime


class SubjectTestsUpdate(SQLModel):
    test: Optional[str] = None
    questiontyp: Optional[str] = None
