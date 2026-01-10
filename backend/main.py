import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from sqlmodel import Session

from db.seed_data import seed_database
from db.database import create_db_and_tables, engine
from routers.users import router as users_router
from routers.subjects import router as subject_router
from routers.subject_tests import router as subject_tests_router
from routers.learning_sessions import router as learning_sessions_router
from routers.stats import router as stats_router
from routers.attempts import router as attempt_router

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TESTING") != "1":
        create_db_and_tables()
        with Session(engine) as session:
            seed_database(session)
    yield

app = FastAPI(lifespan=lifespan, title="SmartLearning Backend", description="Backend API for SmartLearning Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users_router)
app.include_router(subject_router)
app.include_router(subject_tests_router)
app.include_router(attempt_router)
app.include_router(stats_router)
app.include_router(learning_sessions_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the SmartLearning Backend!"}
