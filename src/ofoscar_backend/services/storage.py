from urllib.parse import urlparse

from uuid import uuid4

import boto3

from ofoscar_backend.core.config import settings

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
)

def upload_image(
    file_data,
    file_size:int,
    content_type: str,
    file_extension: str,
) -> str:
  object_name = f"projects/{uuid4()}.{file_extension}"

  s3.upload_fileobj(
        file_data,
        settings.s3_bucket_name,
        object_name,
        ExtraArgs={
            "ContentType": content_type,
        },
    )

  return f"{settings.s3_public_url}/{object_name}"

def get_object_name_from_url(url: str) -> str:
    parsed = urlparse(url)

    return parsed.path.lstrip("/")

def delete_image(url: str) -> None:
    object_name = get_object_name_from_url(url)

    s3.delete_object(
        Bucket=settings.s3_bucket_name,
        Key=object_name,
    )