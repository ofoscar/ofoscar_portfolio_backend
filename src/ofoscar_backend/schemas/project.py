from pydantic import BaseModel

class ProjectCreate(BaseModel):
  title: str
  description: str
  github_url: str | None = None
  demo_url: str | None = None
  published: bool = False

class ProjectResponse(ProjectCreate):
  id:int

  model_config = {
    "from_attributes": True
  }
  