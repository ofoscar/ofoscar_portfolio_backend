from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  secret_key: str
  admin_email: str
  admin_password_hash: str
  database_url: str

  minio_endpoint: str
  minio_access_key: str
  minio_secret_key: str
  minio_bucket: str
  minio_secure: bool = False
  minio_public_url: str
  
  model_config = SettingsConfigDict(
    env_file=".env.app",
    env_file_encoding="utf_8",
  )

settings = Settings()