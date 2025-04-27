from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Welcome to the HMCTS Task Tracker API!"