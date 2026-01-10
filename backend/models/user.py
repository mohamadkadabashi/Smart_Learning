from datetime import datetime, timezone
from typing import Optional, Annotated
from pydantic import EmailStr, StringConstraints
from sqlmodel import Column, DateTime, SQLModel, Field

# Base model for user with common fields
class UserBase(SQLModel):
    username: Annotated[str,
        StringConstraints(strip_whitespace=True, min_length=1)] = Field(nullable=False, unique=True)
    email: EmailStr = Field(nullable=False, unique=True)

    daily_goal: int = Field(default=1, ge=1, nullable=False)
    streak_enabled: bool = Field(default=True, nullable=False)

# User model extending the base with additional fields
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(nullable=False)
    
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    
# Model for creating a new user
class UserCreate(UserBase):
    password: Annotated[str, 
        StringConstraints(strip_whitespace=True, min_length=8)] = Field(nullable=False)

# Model for reading user information
class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

# Model for updating user information
class UserUpdate(SQLModel):
    username: Annotated[
        Optional[str],
        StringConstraints(strip_whitespace=True, min_length=1)
    ] = None
    email: Optional[EmailStr] = None
    password: Annotated[
        Optional[str],
        StringConstraints(strip_whitespace=True, min_length=8)
    ] = None

    daily_goal: Optional[int] = Field(default=None, ge=1)
    streak_enabled: Optional[bool] = None


class LoginInput(SQLModel):
    identifier: str
    password: str
