

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ofoscar_backend.database.session import get_db
from ofoscar_backend.models.video import Video
from ofoscar_backend.routers.auth import get_current_admin
from ofoscar_backend.schemas.video import VideoCreate, VideoResponse, VideoUpdate


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

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int,
    db: Session = Depends(get_db)
              ):
  video = db.get(Video, video_id)

  if video is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Video not found"
    )

  return video

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

@router.patch("/{video_id}", response_model=VideoResponse)
def update_video(
  video_id: int,
  video_update: VideoUpdate,
  db: Session = Depends(get_db),
  current_admin: str = Depends(get_current_admin),
):
  video = db.get(Video, video_id)

  if video is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Video not found",
    )

  update_data = video_update.model_dump(exclude_unset=True, exclude_none=True)
  for field, value in update_data.items():
    setattr(video, field, value)

  db.commit()
  db.refresh(video)
  return video
