# conftest.py
import pytest
import approvaltests
from approvaltests.core import Options
from approvaltests.reporters import DiffReporter
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool  # Good for in-memory SQLite

from app import app
from models import get_session

# Do not remove, side-effect import for test db table generation
# pylint:disable=W0401,W0611,W0614
from models.entity import *


@pytest.fixture(name="session")
def session_fixture():
    """
    Provides a database session for each test, with a transaction that rolls back.
    This ensures each test starts with a clean database state.
    """
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session  # Provide the session to the test
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Provides a FastAPI test client configured to use the transactional session.
    """
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="verify")
def verify_fixture():
    def verify_in_goldens(received_text: str):
        approvaltests.set_default_reporter(DiffReporter())
        approvaltests.verify(received_text)

    return verify_in_goldens
