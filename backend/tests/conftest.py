import pytest
from sqlmodel import SQLModel, create_engine, Session
from src.db.database import get_session
from src.main import app
from src.models.task import Task  # Import models so SQLModel knows about them


# Create an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """
    Set up a fresh test database for each test function.
    Creates all tables before the test and drops them after.
    """
    # Create all tables
    SQLModel.metadata.create_all(test_engine)

    # Override the get_session dependency to use test database
    def get_test_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session

    yield

    # Clean up: drop all tables and clear overrides
    SQLModel.metadata.drop_all(test_engine)
    app.dependency_overrides.clear()


@pytest.fixture
def test_session():
    """
    Provide a test database session.
    """
    with Session(test_engine) as session:
        yield session
