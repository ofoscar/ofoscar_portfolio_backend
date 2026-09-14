from sqlalchemy import Boolean, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ofoscar_backend.database.base import Base

class Project(Base):
  __tablename__ = "projects"

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(200))
  description: Mapped[str] = mapped_column(Text)

  github_url: Mapped[str | None] = mapped_column(
    String(500),
    nullable=True,
  )

  demo_url: Mapped[str | None] = mapped_column(
    String(500),
    nullable=True,
  )

  published: Mapped[bool] = mapped_column(
    Boolean,
    default=False
  )

  tags: Mapped[list[str]] = mapped_column(
    JSON,
    default = list,
  )

  highlights: Mapped[list[str]] = mapped_column(
    JSON,
    default = list
  )