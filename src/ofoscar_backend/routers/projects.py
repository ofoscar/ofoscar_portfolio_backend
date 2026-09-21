from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ofoscar_backend.routers.auth import get_current_admin
from ofoscar_backend.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from ofoscar_backend.models.project import Project
from ofoscar_backend.models.project_image import ProjectImage
from ofoscar_backend.services.storage import delete_image
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

@router.patch(
        "/{project_id}",
        response_model=ProjectResponse
)
def edit_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    update_data = project_update.model_dump(
        exclude_unset=True,
        exclude={"images"},
    )

    for field, value in update_data.items():
        setattr(project, field, value)

    if project_update.images is not None:
        project.images = [
            ProjectImage(
                image_url=image.image_url,
                description=image.description,
            )
            for image in project_update.images
        ]

    db.commit()
    db.refresh(project)

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

    if project.cover_image_url:
        delete_image(project.cover_image_url)

    if project.images: 
        for image in project.images:
            delete_image(image.image_url)

    db.delete(project)
    db.commit()