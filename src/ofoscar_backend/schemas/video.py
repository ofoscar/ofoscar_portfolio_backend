
from datetime import datetime
from enum import Enum

from pydantic import BaseModel

class VideoType(str, Enum):
  SHORT_FORM = "Short form"
  YOUTUBE_VIDEO = "Youtube video"

class VideoCategory(str, Enum):
  SOFTWARE_DEVELOPMENT = "Software development"

class VideoCreate(BaseModel):
  title: str
  slug: str
  type: VideoType
  date_uploaded: datetime
  category: VideoCategory
  link: str

class VideoUpdate(BaseModel):
  title: str | None = None
  slug: str | None = None
  type: VideoType | None = None
  date_uploaded: datetime | None = None
  category: VideoCategory | None = None
  link: str | None = None

class VideoResponse(VideoCreate):
  id: int

  model_config = {
    "from_attributes": True
  }
