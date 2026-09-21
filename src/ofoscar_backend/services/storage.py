from urllib.parse import urlparse

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

def get_object_name_from_url(url: str) -> str:
    parsed = urlparse(url)

    path = parsed.path.lstrip("/")

    bucket_prefix = f"{settings.minio_bucket}/"

    if not path.startswith(bucket_prefix):
        raise ValueError("URL does not belong to configured MinIO bucket")

    return path.removeprefix(bucket_prefix)


def delete_image(url: str) -> None:
    object_name = get_object_name_from_url(url)

    client.remove_object(
        bucket_name=settings.minio_bucket,
        object_name=object_name,
    )