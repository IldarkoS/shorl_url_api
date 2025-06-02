import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.config import settings
from src.core.models.base import Base

if TYPE_CHECKING:
    from src.users.domain.user import User
    from src.clicks.domain.click import Click


def default_expires():
    return datetime.datetime.now() + datetime.timedelta(
        days=settings.DAYS_UNTIL_EXPIRED
    )


class URL(Base):
    __tablename__ = "urls"

    original_url: Mapped[str] = mapped_column(String())
    code: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=default_expires(),
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(back_populates="urls")
    clicks: Mapped[list["Click"]] = relationship(back_populates="url")
