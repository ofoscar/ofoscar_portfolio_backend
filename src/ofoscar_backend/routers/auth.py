from fastapi import APIRouter, HTTPException, status
from ofoscar_backend.core.config import settings

from ofoscar_backend.core.security import (
  create_access_token,
  verify_password,
)
from ofoscar_backend.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(
  prefix="/auth",
  tags=["Authentication"],
)

ADMIN_EMAIL = settings.admin_email

ADMIN_PASSWORD_HASH = settings.admin_password_hash

@router.post("/login", response_model= TokenResponse)
def login(credentials: LoginRequest):
  if credentials.email != ADMIN_EMAIL:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials",
    )

  if not verify_password(
    credentials.password,
    ADMIN_PASSWORD_HASH,
  ):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials",
    )

  access_token = create_access_token(
    subject=credentials.email,
  )

  return TokenResponse(
    access_token=access_token,
  )