from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  secret_key: str
  admin_email: str
  admin_password_hash: str
  database_url: str
  
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf_8",
  )

settings = Settings()