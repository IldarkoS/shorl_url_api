from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.urls.domain.url import URL


class User(Base):
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    urls: Mapped[list["URL"]] = relationship(back_populates="user")
