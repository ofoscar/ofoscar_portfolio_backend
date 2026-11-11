from fastapi.testclient import TestClient
from ofoscar_backend.main import app
from ofoscar_backend.routers.auth import get_current_admin


def override_get_current_admin():
    return "test@example.com"


app.dependency_overrides[get_current_admin] = override_get_current_admin

client = TestClient(app)


def post_payload(title="Test post"):
    return {
        "title": title,
        "cover_image_url": "https://example.com/cover.jpg",
        "published": False,
        "hook": "A short introduction",
        "slug": "test-post",
        "category": "engineering",
        "content": [
            {"title": "First section", "content": "Section text"},
            {"title": "Second section", "content": "More text"},
        ],
    }


def test_create_post():
    response = client.post("/posts", json=post_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test post"
    assert data["slug"] == "test-post"
    assert data["content"] == post_payload()["content"]


def test_get_posts():
    client.post("/posts", json=post_payload())

    response = client.get("/posts")

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 1
    assert posts[0]["title"] == "Test post"


def test_create_post_rejects_duplicate_title():
    client.post("/posts", json=post_payload())

    response = client.post("/posts", json=post_payload())

    assert response.status_code == 409
    assert response.json()["detail"] == "A post with this title already exists"
