from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.db.session import get_db
from app.models.tasks import Base, DBTask
from app.schemas.task import TaskStatus

@pytest.fixture(name="session")
def session_fixture():

    # Create in-memory SQLite db
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session with sample data
    with sessionmaker(autocommit=False, autoflush=False, bind=engine)() as session:
        for i in range(5):
            task = DBTask(
                title=f"Task {i}",
                description=f"Description for task {i}",
                status=TaskStatus.PENDING,
                due_date=datetime(year=2025, month=4, day=i+1).isoformat()
            )
            session.add(task)
        session.commit()
        yield session
    

@pytest.fixture(name="client")
def client_fixture(session: Session):
    app.dependency_overrides[get_db] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Welcome to the HMCTS Task Tracker API!"


def is_isoformat(date_string: str) -> bool:
    try:
        datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False


def test_get_all_tasks(client: TestClient):
    response = client.get("api/v1/tasks/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    for task in data:
        assert isinstance(task["id"], int)
        assert isinstance(task["title"], str)
        assert isinstance(task["description"], str) or task["description"] is None
        assert task["status"] in TaskStatus.__members__.values()
        assert isinstance(task["due_date"], str)
        assert is_isoformat(task["due_date"])

