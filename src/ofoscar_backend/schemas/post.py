
from pydantic import BaseModel
class PostSection(BaseModel):
  title: str
  content: str

class PostCreate(BaseModel):
  title: str
  cover_image_url: str
  published: bool
  hook: str
  slug: str
  category: str
  content: list[PostSection]

class PostResponse(PostCreate):
  id: int

  model_config = {
    "from_attributes": True
  }


