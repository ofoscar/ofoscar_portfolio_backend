from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  secret_key: str
  admin_email: str
  admin_password_hash: str
  database_url: str

  aws_access_key_id: str
  aws_secret_access_key: str
  aws_region: str

  s3_bucket_name: str
  s3_public_url: str
  
  model_config = SettingsConfigDict(
    env_file=".env.app",
    env_file_encoding="utf_8",
  )

settings = Settings()