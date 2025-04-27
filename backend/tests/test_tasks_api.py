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


# Helper function to verify datetime string format
def is_isoformat(date_string: str) -> bool:
    try:
        datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False


def test_create_task(client: TestClient, session: Session):
    # Check inital count of tasks to verify new task creation
    starting_count = session.query(DBTask).count()

    # Create a new (valid) task
    new_task = {
        "title": "New Task",
        "description": "Description for new task",
        "status": TaskStatus.PENDING,
        "due_date": datetime(year=2025, month=4, day=25).isoformat()
    }
    response = client.post("api/v1/tasks/", json=new_task)

    # Check response status and data matching
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == new_task["title"]
    assert data["description"] == new_task["description"]
    assert data["status"] == new_task["status"]
    assert data["due_date"] == new_task["due_date"]

    # Check task count increased
    new_count = session.query(DBTask).count()
    assert new_count == starting_count + 1


def test_create_task_invalid(client: TestClient):
    # Create a new task with invalid data
    new_task_invalid_status = {
        "title": "New Task",
        "description": "Description for new task",
        "status": "invalid_status",  
        "due_date": datetime(year=2025, month=4, day=25).isoformat()
    }
    response = client.post("api/v1/tasks/", json=new_task_invalid_status)
    assert response.status_code == 422, response.text

    # Create a new task with missing title
    new_task_invalid_title = {
        "title": "", 
        "description": "Description for new task",
        "status": TaskStatus.PENDING,
        "due_date": datetime(year=2025, month=4, day=25).isoformat()
    }
    response = client.post("api/v1/tasks/", json=new_task_invalid_title)
    assert response.status_code == 422, response.text


def test_get_task_by_id(client: TestClient):

    # Assuming the first task has id=1
    # and we have already created 5 tasks in the fixture
    response = client.get("api/v1/tasks/1")

    # Check response dtatus and expected data
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Task 0"
    assert data["description"] == "Description for task 0"
    assert data["status"] == TaskStatus.PENDING
    assert is_isoformat(data["due_date"])


def test_get_task_not_found(client: TestClient):

    # Attempt to get a task that does not exist
    # Assuming we have only created 5 tasks with ids 0-4
    response = client.get("api/v1/tasks/999")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Task not found"


def test_get_all_tasks(client: TestClient):
    response = client.get("api/v1/tasks/")
    assert response.status_code == 200, response.text
    data = response.json()

    # Check if the response contains a list of tasks
    # and each task has the expected fields
    assert isinstance(data, list)
    for task in data:
        assert isinstance(task["id"], int)
        assert isinstance(task["title"], str)
        assert isinstance(task["description"], str) or task["description"] is None
        assert task["status"] in TaskStatus.__members__.values()
        assert isinstance(task["due_date"], str)
        assert is_isoformat(task["due_date"])


def test_update_task_status(client: TestClient):
    # Assuming the first task has id=1
    # and we have already created 5 tasks in the fixture
    task_id = 1

    # Update the status of the task
    new_status = TaskStatus.COMPLETED
    response = client.patch(f"api/v1/tasks/{task_id}", json={"status": new_status})

    # Check response status and updated data
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == task_id
    assert data["status"] == new_status


def test_update_task_status_not_found(client: TestClient):

    # Attempt to update a task that does not exist
    task_id = 999
    new_status = TaskStatus.COMPLETED
    response = client.patch(f"api/v1/tasks/{task_id}", json={"status": new_status})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Task not found"


def test_update_task_status_invalid(client: TestClient):

    # Attempt to update a task with an invalid status
    task_id = 1
    new_status = "invalid_status"
    response = client.patch(f"api/v1/tasks/{task_id}", json={"status": new_status})
    assert response.status_code == 422, response.text


def test_delete_task(client: TestClient):

    task_id = 1
    response = client.delete(f"api/v1/tasks/{task_id}")
    assert response.status_code == 204, response.text

    response = client.get(f"api/v1/tasks/{task_id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Task not found"



