
from datetime import date
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
  date_uploaded: date
  category: VideoCategory

class VideoResponse(VideoCreate):
  id: int

  model_config = {
    "from_attributes": True
  }