from fastapi.testclient import TestClient
from ofoscar_backend.main import app
from ofoscar_backend.routers.auth import get_current_admin

def override_get_current_admin():
    return "test@example.com"

app.dependency_overrides[get_current_admin] = override_get_current_admin

client = TestClient(app)

def test_create_project():
  response = client.post(
    "/projects",
    json ={
      "title": "Test",
      "description": "Description test"
    }
  )

  assert response.status_code == 201

  data = response.json()

  assert data["title"] == "Test"
  assert data["description"] == "Description test"


def test_get_projects():
  client.post(
        "/projects",
        json={
            "title": "Test",
            "description": "Description test",
        },
    )

  response = client.get("/projects")

  assert response.status_code == 200

  projects = response.json()

  assert len(projects) == 1
  assert projects[0]["title"] == "Test"

