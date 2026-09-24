import pytest

from ofoscar_backend.database.session import SessionLocal
from ofoscar_backend.models.project import Project
from ofoscar_backend.models.project_image import ProjectImage


@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    db.query(ProjectImage).delete()
    db.query(Project).delete()

    db.commit()
    db.close()

    yield