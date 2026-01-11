import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient

from main import app
from db.database import get_session

# Configure a separate database for testing
TEST_DATABASE_URL = "sqlite:///tests/db/test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)


@pytest.fixture(name="session")
def session_fixture():
    # Create the database and the tables
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):

    def override_get_session():
        yield session

    # Override the get_session dependency
    app.dependency_overrides[get_session] = override_get_session

    client = TestClient(app)
    yield client

    # Clean up Dependency Override
    app.dependency_overrides.clear()
