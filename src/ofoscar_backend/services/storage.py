from uuid import uuid4

from minio import Minio

from ofoscar_backend.core.config import settings

client = Minio(
  settings.minio_endpoint,
  access_key=settings.minio_access_key,
  secret_key=settings.minio_secret_key,
  secure=settings.minio_secure,
)

def upload_image(
    file_data,
    file_size:int,
    content_type: str,
    file_extension: str,
) -> str:
  filename = f"projects/{uuid4()}.{file_extension}"

  client.put_object(
    bucket_name=settings.minio_bucket,
    object_name=filename,
    data=file_data,
    length=file_size,
    content_type=content_type
  )

  return(
    f"{settings.minio_public_url}/"
    f"{settings.minio_bucket}/"
    f"{filename}"
  )

def delete_object(object_name:str) -> None:
  client.remove_object(
    bucket_name=settings.minio_bucket,
    object_name=object_name
  )