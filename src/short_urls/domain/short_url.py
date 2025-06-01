import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.config import settings
from src.core.models.base import Base


def default_expires():
    return datetime.datetime.now() + datetime.timedelta(days=settings.DAYS_UNTIL_EXPIRED)

class ShortURL(Base):
    __tablename__ = 'short_urls'

    original_url: Mapped[str] = mapped_column(String())
    short_url: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=default_expires(),
    )
    is_active: Mapped[bool] = mapped_column(default=True)