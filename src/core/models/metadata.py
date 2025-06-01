__all__ = (
    "Base",
    "ShortURL",
    "User",
)

from src.core.models.base import Base
from src.short_urls.domain.short_url import ShortURL
from src.users.domain.user import User


metadata = Base.metadata
