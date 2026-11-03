from fastapi.testclient import TestClient

from ofoscar_backend.main import app
from ofoscar_backend.routers.auth import get_current_admin


def override_get_current_admin():
    return "test@example.com"


app.dependency_overrides[get_current_admin] = override_get_current_admin
client = TestClient(app)

VIDEO_PAYLOAD = {
    "title": "Video test",
    "slug": "video-test",
    "type": "Short form",
    "date_uploaded": "2026-10-30T18:14:21.421000Z",
    "category": "Software development",
    "link": "https://example.com/video",
}


def create_video():
    return client.post("/videos", json=VIDEO_PAYLOAD)


def test_create_video_returns_created_video():
    response = create_video()

    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["id"], int)
    for field, value in VIDEO_PAYLOAD.items():
        assert data[field] == value


def test_get_videos_returns_saved_videos():
    created = create_video()
    assert created.status_code == 201

    response = client.get("/videos")

    assert response.status_code == 200
    assert response.json() == [created.json()]


def test_get_video_returns_video_by_id():
    created = create_video()
    assert created.status_code == 201
    video = created.json()

    response = client.get(f"/videos/{video['id']}")

    assert response.status_code == 200
    assert response.json() == video


def test_get_video_returns_404_when_video_does_not_exist():
    response = client.get("/videos/999999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Video not found"}


def test_create_video_rejects_invalid_type():
    payload = {**VIDEO_PAYLOAD, "type": "Livestream"}

    response = client.post("/videos", json=payload)

    assert response.status_code == 422


def test_create_video_requires_all_schema_fields():
    payload = {key: value for key, value in VIDEO_PAYLOAD.items() if key != "slug"}

    response = client.post("/videos", json=payload)

    assert response.status_code == 422
