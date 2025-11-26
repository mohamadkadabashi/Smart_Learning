from typing import List
from fastapi import APIRouter, HTTPException, Depends
<<<<<<< HEAD
<<<<<<< HEAD
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.user import User, UserCreate, UserRead, UserUpdate, LoginInput
=======
from sqlmodel import Session, select
from database import get_session
from models.user import User, UserCreate, UserRead, UserUpdate
>>>>>>> 49a442e (create the API-Endpoints and DB-Models)
=======
from sqlmodel import SQLModel, Session, select
from database import get_session
from models.user import User, UserCreate, UserRead, UserUpdate, LoginInput
>>>>>>> 81dc65d (modify UserBase to have only username and email. LoginInput-Model to input username or email)
import bcrypt

router = APIRouter(prefix="/users", tags=["users"])

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    email_exists = session.exec(select(User).where(User.email == user_create.email)).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    username_exists = session.exec(select(User).where(User.username == user_create.username)).first()
    if username_exists:
        raise HTTPException(status_code=400, detail="Username already taken")
<<<<<<< HEAD
<<<<<<< HEAD
=======

    first_name_exists = session.exec(select(User).where(User.first_name == user_create.first_name)).first()
    if first_name_exists:
        raise HTTPException(status_code=400, detail="First name already in use")
    
    last_name_exists = session.exec(select(User).where(User.last_name == user_create.last_name)).first()
    if last_name_exists:
        raise HTTPException(status_code=400, detail="Last name already in use")
>>>>>>> 49a442e (create the API-Endpoints and DB-Models)
=======
>>>>>>> 81dc65d (modify UserBase to have only username and email. LoginInput-Model to input username or email)
    
    hashed_password = hash_password(user_create.password)
    
    db_user = User(
        username=user_create.username,
<<<<<<< HEAD
<<<<<<< HEAD
=======
        first_name=user_create.first_name,
        last_name=user_create.last_name,
>>>>>>> 49a442e (create the API-Endpoints and DB-Models)
=======
>>>>>>> 81dc65d (modify UserBase to have only username and email. LoginInput-Model to input username or email)
        email=user_create.email,
        password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserRead])
def read_users(
    session: Session = Depends(get_session)
):
    users = session.exec(select(User)).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
    
    if user_update.first_name is not None:
        user.first_name = user_update.first_name
    
    if user_update.last_name is not None:
        user.last_name = user_update.last_name
>>>>>>> 49a442e (create the API-Endpoints and DB-Models)
=======
>>>>>>> 81dc65d (modify UserBase to have only username and email. LoginInput-Model to input username or email)

    if user_update.password is not None:
        user.password = hash_password(user_update.password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    return None

@router.post("/login")
<<<<<<< HEAD
<<<<<<< HEAD
def login_user( 
    login_data: LoginInput,
    session: Session = Depends(get_session)
):
    identifier = login_data.identifier
    password = login_data.password
    user = session.exec(select(User).where(
        (User.email == identifier) | (User.username == identifier))
    ).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email/username or password")
=======
def login_user(
    email: str,
    password: str,
=======
def login_user( 
    login_data: LoginInput,
>>>>>>> 81dc65d (modify UserBase to have only username and email. LoginInput-Model to input username or email)
    session: Session = Depends(get_session)
):
    identifier = login_data.identifier
    password = login_data.password
    user = session.exec(select(User).where(
        (User.email == identifier) | (User.username == identifier))
    ).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
<<<<<<< HEAD
        raise HTTPException(status_code=401, detail="Invalid email or password")
>>>>>>> 49a442e (create the API-Endpoints and DB-Models)
=======
        raise HTTPException(status_code=401, detail="Invalid email/username or password")
>>>>>>> 81dc65d (modify UserBase to have only username and email. LoginInput-Model to input username or email)
    
    return {"message": "Login successful", "user_id": user.id}