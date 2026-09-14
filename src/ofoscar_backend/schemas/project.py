from typing import Annotated

from pydantic import BaseModel,Field

Tag = Annotated[
  str,
  Field(
    min_length = 1,
    max_length = 25
  )
]

class ProjectCreate(BaseModel):
  title: str
  description: str
  github_url: str | None = None
  demo_url: str | None = None
  published: bool = False
  tags: list[Tag] = Field(
    default_factory = list,
    max_length = 10
  )

class ProjectResponse(ProjectCreate):
  id:int

  model_config = {
    "from_attributes": True
  }
  