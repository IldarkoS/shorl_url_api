__all__ = (
    "Base",
    "URL",
    "User",
)

from src.core.models.base import Base
from src.urls.domain.url import URL
from src.users.domain.user import User


metadata = Base.metadata
