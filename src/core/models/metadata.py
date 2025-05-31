__all__ = (
    "Base",
    "ShortURL",
)

from src.core.models import Base
from src.short_urls.models.short_url import ShortURL

metadata = Base.metadata
