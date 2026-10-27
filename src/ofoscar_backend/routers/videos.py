

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ofoscar_backend.database.session import get_db
from ofoscar_backend.models.video import Video
from ofoscar_backend.routers.auth import get_current_admin
from ofoscar_backend.schemas.video import VideoCreate, VideoResponse


router = APIRouter(
  prefix = "/videos",
  tags=["Videos"]
)

@router.get("", response_model=list[VideoResponse])
def get_videos(
  db: Session = Depends(get_db),
):
  return(
    db.query(Video)
    .all()
  )

@router.post("", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video(
  video: VideoCreate,
  db: Session = Depends(get_db),
  current_admin: str = Depends(get_current_admin)
):
  new_video = Video(
    **video.model_dump()
  )

  db.add(new_video)
  db.commit()
  db.refresh(new_video)

  return new_video
