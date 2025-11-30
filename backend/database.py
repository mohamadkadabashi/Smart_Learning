from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "postgresql+psycopg2://myapp_user:mypassword@db:5432/myapp"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]