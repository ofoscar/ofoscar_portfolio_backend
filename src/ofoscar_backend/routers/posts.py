
from fastapi import APIRouter, Depends, HTTPException,status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ofoscar_backend.models.post import Post
from ofoscar_backend.routers.auth import get_current_admin
from ofoscar_backend.schemas.post import PostCreate, PostResponse

from ofoscar_backend.database.session import get_db

router = APIRouter(
  prefix='/posts',
  tags=["Posts"]
)

@router.get("", response_model=list[PostResponse])
def get_posts(
  db: Session = Depends(get_db),
  current_admin: str = Depends(get_current_admin)
):
  return (
    db.query(Post)
    .all()
  )

@router.post(
  "",
  response_model=PostResponse,
  status_code=status.HTTP_201_CREATED
)
def create_post(
  post_data: PostCreate,
  db: Session = Depends(get_db),
  current_admin: str = Depends(get_current_admin)
):
  existing = db.query(Post).filter(Post.title == post_data.title).first()

  if existing:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="A post with this title already exists",
    )
  
  post = Post(**post_data.model_dump())
  db.add(post)

  try:
    db.commit()
  except IntegrityError:
    db.rollback()
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="A post with this title already exists"
    )

  db.refresh(post)
  return post