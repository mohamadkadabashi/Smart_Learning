from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from database import SessionDep
from models.user import User, UserCreate, UserRead, UserUpdate, LoginInput
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    user_create: UserCreate,
    session: SessionDep
):
    email_exists = session.exec(select(User).where(User.email == user_create.email)).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    username_exists = session.exec(select(User).where(User.username == user_create.username)).first()
    if username_exists:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = hash_password(user_create.password)
    
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserRead])
def read_users(
    session: SessionDep
):
    users = session.exec(select(User)).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    session: SessionDep
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: SessionDep
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.username is not None:
        username_exists = session.exec(select(User).where(User.username == user_update.username, User.id != user_id)).first()
        if username_exists:
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = user_update.username
    
    if user_update.email is not None:
        email_exists = session.exec(select(User).where(User.email == user_update.email, User.id != user_id)).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = user_update.email

    if user_update.password is not None:
        user.password = hash_password(user_update.password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    session: SessionDep
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    return None

@router.post("/login")
def login_user( 
    login_data: LoginInput,
    session: SessionDep
):
    identifier = login_data.identifier
    password = login_data.password
    user = session.exec(select(User).where(
        (User.email == identifier) | (User.username == identifier))
    ).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email/username or password")
    
    return {"message": "Login successful", "user_id": user.id}