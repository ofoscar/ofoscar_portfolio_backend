
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ofoscar_backend.database.base import Base


class Video(Base):
  __tablename__ = "videos"

  id: Mapped[int] = mapped_column(primary_key=True)

  title: Mapped[str] = mapped_column(String(200))

  slug: Mapped[str] = mapped_column(String(300))

  type: Mapped[str] = mapped_column(String(200))

  date_uploaded: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
  )

  category: Mapped[str] = mapped_column(
    String(200)
  )
