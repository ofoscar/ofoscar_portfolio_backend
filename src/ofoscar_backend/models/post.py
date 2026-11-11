from sqlalchemy import JSON, String, Boolean
from ofoscar_backend.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Post(Base):
  __tablename__ = "posts"

  id: Mapped[int] = mapped_column(primary_key=True)

  title: Mapped[str] = mapped_column(String(60), unique=True)

  cover_image_url: Mapped[str | None] = mapped_column(
    String(1000), 
    nullable=True
  )
  
  published: Mapped[bool] = mapped_column(
    Boolean,
    default=False
  )

  hook: Mapped[str] = mapped_column(
    String(300)
  )

  slug: Mapped[str] = mapped_column(
    String(200)
  )

  category: Mapped[str] = mapped_column(
    String(20)
  )

  content: Mapped[list[dict[str,str]]] = mapped_column(
    JSON,
    nullable=False,
    default=list
  )
