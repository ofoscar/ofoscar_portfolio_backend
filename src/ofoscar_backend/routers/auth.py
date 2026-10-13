from fastapi import APIRouter, Depends, HTTPException, status, Response,Cookie 
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from ofoscar_backend.core.config import settings

from ofoscar_backend.core.security import (
  create_access_token,
  decode_access_token,
  verify_password,
)

router = APIRouter(
  prefix="/auth",
  tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False,
)

ADMIN_EMAIL = settings.admin_email

def get_auth_token(
    bearer_token: Annotated[
        str | None,
        Depends(oauth2_scheme),
    ],
    session: Annotated[
        str | None,
        Cookie(),
    ] = None,
) -> str:
    token = bearer_token or session

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return token

@router.post("/login", status_code=status.HTTP_200_OK)
def login(
  response: Response,
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

  response.set_cookie(
        key="session",
        value=access_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=60 * 60,
        path="/",
    )

  return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response):
   response.delete_cookie(
      key="session",
      path="/",
      secure=settings.cookie_secure,
      httponly=True,
      samesite="lax"
   )

   return {"message": "Logged out"}

def get_current_admin(
    token: str = Depends(get_auth_token),
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