from io import BytesIO

from fastapi import (
  APIRouter,
  Depends,
  HTTPException,
  UploadFile,
  status
)

from ofoscar_backend.routers.auth import get_current_admin
from ofoscar_backend.services.storage import upload_image

router = APIRouter(
  prefix="/uploads",
  tags=["Uploads"]
)

ALLOWED_IMAGE_TYPES = {
  "image/jpeg",
  "image/png",
  "image/jpg",
  "image/webp"
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024

CONTENT_TYPE_EXTENSIONS = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}

@router.post("/images")
async def upload_project_image(
  file: UploadFile,
  current_admin: str = Depends(get_current_admin)
):
  if file.content_type not in ALLOWED_IMAGE_TYPES:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Unsupported image type",
    )

  contents = await file.read()

  if len(contents) > MAX_IMAGE_SIZE:
    raise HTTPException(
      status_code=status.HTTP_413_CONTENT_TOO_LARGE,
      detail="Image must be smaller than 5 MB"
    )

  extension = CONTENT_TYPE_EXTENSIONS[file.content_type]

  image_url = upload_image(
    file_data=BytesIO(contents),
    file_size=len(contents),
    content_type=file.content_type,
    file_extension=extension
  )

  return {
    "url": image_url
  }