from fastapi.testclient import TestClient
from ofoscar_backend.main import app

client = TestClient(app)

def test_create_project():
  response = client.post(
    "/projects",
    json ={
      "title": "Test",
      "description": "Description test"
    }
  )

  assert response.status_code == 200
  assert response.json()["title"] == "Test"

def test_get_projects():
  response = client.get("/projects")

  assert response.status_code == 200
  assert len(response.json()) == 1
  assert response.json()[0]["title"] == "Test"

