from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from ofoscar_backend.core.config import settings
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
  return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
  return password_hash.verify(password, hashed_password)

def create_access_token(subject: str) -> str:
  expires_at = datetime.now(timezone.utc) + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
  )

  payload = {
    "sub": subject,
    "exp": expires_at,
  }

  return jwt.encode(
    payload,
    SECRET_KEY,
    algorithm=ALGORITHM
  )

def decode_access_token(token:str) -> str:
  try:
    payload = jwt.decode(
      token,
      settings.secret_key,
      algorithms=[ALGORITHM],
    )

    subject = payload.get("sub")

    if subject is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
      )

    return subject

  except InvalidTokenError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token",
    )
  