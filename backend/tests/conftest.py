import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient

from backend.main import app
from backend.database import get_session  # das überschreiben wir


# 1) Test-Datenbank (SQLite-Datei im Projektordner)
TEST_DATABASE_URL = "sqlite:///backend/tests/db/test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # weniger Spam im Test-Output
)


@pytest.fixture(name="session")
def session_fixture():
    # Datenbank für jeden Testlauf frisch aufsetzen
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    """
    FastAPI TestClient, der unsere Test-Session verwendet
    statt der echten Postgres-Session.
    """

    def override_get_session():
        yield session

    # Dependency Override registrieren
    app.dependency_overrides[get_session] = override_get_session

    client = TestClient(app)
    yield client

    # Overrides wieder aufräumen
    app.dependency_overrides.clear()
