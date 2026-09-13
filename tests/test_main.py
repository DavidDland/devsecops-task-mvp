from fastapi.testclient import TestClient
from app.main import app, tasks

client = TestClient(app)

def setup_function():
    tasks.clear()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_list_task():
    create_response = client.post("/tasks", json={"title": "Learn Kubernetes"})
    assert create_response.status_code == 201
    assert create_response.json()["title"] == "Learn Kubernetes"

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

def test_reject_blank_task():
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400
