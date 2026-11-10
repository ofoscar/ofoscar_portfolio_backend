
from fastapi import APIRouter, Depends,status

from sqlalchemy.orm import Session

from ofoscar_backend.models.post import Post
from ofoscar_backend.routers.auth import get_current_admin
from ofoscar_backend.schemas.post import PostCreate, PostResponse

from ofoscar_backend.database.session import get_db

router = APIRouter(
  prefix='/posts',
  tags=["Posts"]
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
  post = Post(**post_data.model_dump())

  db.add(post)
  db.commit()
  db.refresh(post)

  return post