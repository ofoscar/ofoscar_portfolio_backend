from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from ofoscar_backend.core.config import settings

from ofoscar_backend.core.security import (
  create_access_token,
  decode_access_token,
  verify_password,
)
from ofoscar_backend.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(
  prefix="/auth",
  tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

ADMIN_EMAIL = settings.admin_email

@router.post("/login", response_model= TokenResponse)
def login(
  form_data: OAuth2PasswordRequestForm = Depends(),
):
  if form_data.username != settings.admin_email:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials"
    )

  if not verify_password(
    form_data.password,
    settings.admin_password_hash,
  ):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials",
    )

  access_token = create_access_token(
    subject=form_data.username,
  )

  return {
    "access_token": access_token,
    "token_type": "bearer",
  }

def get_current_admin(
    token: str = Depends(oauth2_scheme),
) -> str:
  email = decode_access_token(token)

  if email != settings.admin_email:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials",
    )

  return email

@router.get("/me")
def get_me(
  current_admin: str = Depends(get_current_admin),
):
  return {
    "email":current_admin
  }