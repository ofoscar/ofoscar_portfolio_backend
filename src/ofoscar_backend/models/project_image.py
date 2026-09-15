from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ofoscar_backend.database.base import Base

class ProjectImage(Base):
  __tablename__ = "project_images"

  id: Mapped[int] = mapped_column(
    primary_key=True
  )

  image_url: Mapped[str] = mapped_column(
    String(1000)
  )

  description: Mapped[str] = mapped_column(
    String(500),
    nullable=True
  )

  project_id: Mapped[int] = mapped_column(
    ForeignKey(
      "projects.id",
      ondelete="CASCADE"
    )
  )

  project: Mapped["Project"] = relationship(
    back_populates="images"
  )