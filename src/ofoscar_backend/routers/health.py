from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from ofoscar_backend.database.session import get_db

router = APIRouter(
  prefix="/health",
  tags=["Health"],
)

@router.get("")
def health(
  db: Session = Depends(get_db)
):
  try:
    db.execute(text("SELECT 1"))
  except Exception as exc:
    raise HTTPException(
      status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
      detail = "Database unavailable"
    ) from exc

  return {
    "status": "ok",
    "database": "ok"
  }
