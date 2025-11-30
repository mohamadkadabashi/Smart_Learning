from datetime import datetime
from typing import Optional
#from pydantic import EmailStr
from sqlmodel import SQLModel, Field

# Model for subjects
class SubjectBase(SQLModel):
    name: str = Field(nullable=False)

class Subject(SubjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class SubjectCreate(SubjectBase):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class SubjectRead(SubjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class SubjectUpdate(SQLModel):
    name: Optional[str] = None
