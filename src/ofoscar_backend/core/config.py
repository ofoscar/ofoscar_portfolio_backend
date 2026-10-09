from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  secret_key: str
  admin_email: str
  admin_password_hash: str
  database_url: str
  cors_origins: str = ""

  aws_region: str
  s3_bucket_name: str
  s3_public_url: str
  
  model_config = SettingsConfigDict(
    env_file=".env.app",
    env_file_encoding="utf_8",
  )

  @property
  def allowed_origins(self) -> list[str]:
    return [
      origin.strip()
      for origin in self.cors_origins.split(",")
      if origin.strip()
    ]

settings = Settings()