__all__ = ("Base", "URL", "User", "Click")

from src.clicks.adapters.model import Click
from src.core.models.base import Base
from src.urls.adapters.model import URL
from src.users.adapters.model import User


metadata = Base.metadata
