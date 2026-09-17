from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ofoscar_backend.routers.auth import get_current_admin
from ofoscar_backend.schemas.project import ProjectCreate, ProjectResponse
from ofoscar_backend.models.project import Project
from ofoscar_backend.models.project_image import ProjectImage

from ofoscar_backend.database.session import get_db

router = APIRouter(
  prefix="/projects",
  tags=["Projects"],
)

projects: list[dict] = []

@router.get("", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db)
):
    return (
      db.query(Project)
      .filter(Project.published.is_(True))
      .all()
      )
    

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    project_data = project.model_dump(
        exclude={"images"}
    )
    
    new_project = Project(
        **project_data
    )

    new_project.images= [
        ProjectImage(
            image_url=image.image_url,
            description=image.description
        )
        for image in project.images
    ]

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int,
    db: Session = Depends(get_db)):
    
    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()