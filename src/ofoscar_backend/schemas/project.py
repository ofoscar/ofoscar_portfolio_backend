from typing import Annotated

from pydantic import BaseModel,Field

class ProjectImageCreate(BaseModel):
  image_url: str
  description: str | None = Field(
    default=None,
    max_length=500
  )

class ProjectImageResponse(ProjectImageCreate):
  id: int

  model_config = {
    "from_attributes": True
  }

Tag = Annotated[
  str,
  Field(
    min_length = 1,
    max_length = 25
  )
]

HighLight = Annotated[
  str,
  Field(
    min_length = 1,
    max_length = 125
  )
]

class ProjectCreate(BaseModel):
  title: str
  description: str
  github_url: str | None = None
  demo_url: str | None = None
  cover_image_url: str | None = None
  published: bool = False
  tags: list[Tag] = Field(
    default_factory = list,
    max_length = 10
  )
  highlights: list[HighLight] = Field(
    default_factory = list,
    max_length = 6
  )

  images: list[ProjectImageCreate] = Field(
    default_factory=list,
    max_length = 15
  )

class ProjectResponse(ProjectCreate):
  id:int

  images: list[ProjectImageResponse]

  model_config = {
    "from_attributes": True
  }
  