from datetime import datetime, timezone
from typing import Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field

# Base model for user with common fields
class UserBase(SQLModel):
    username: str = Field(nullable=False, unique=True)
    email: EmailStr = Field(nullable=False, unique=True)

# User model extending the base with additional fields
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime =Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

# Model for creating a new user
class UserCreate(UserBase):
    password: str = Field(nullable=False)

# Model for reading user information
class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

# Model for updating user information
class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class LoginInput(SQLModel):
    identifier: str
    password: str
