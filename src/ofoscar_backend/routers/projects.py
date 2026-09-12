from fastapi import APIRouter, Depends, HTTPException, status

from ofoscar_backend.routers.auth import get_current_admin
from ofoscar_backend.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(
  prefix="/projects",
  tags=["Projects"],
)

projects: list[dict] = []

@router.get("", response_model=list[ProjectResponse])
def get_projects():
    return [
      project
      for project in projects
      if project["published"] is True
    ]

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project: ProjectCreate,
    current_admin: str = Depends(get_current_admin)
):
    new_project = {
        "id": len(projects) + 1,
        **project.model_dump(),
    }

    projects.append(new_project)

    return new_project

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int):
    project = next(
        (
            project
            for project in projects
            if project["id"] == project_id
            and project["published"] == True
        )
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project