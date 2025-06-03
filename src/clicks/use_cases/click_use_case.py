from datetime import datetime, UTC, timedelta
from typing import Protocol, Self

from src.clicks.adapters.click_repository import ClickRepositoryProtocol
from src.config import settings
from src.urls.adapters.model import URL


class ClickUseCaseProtocol(Protocol):
    async def log_click(self: Self, url_id: int): ...

    async def get_stats(self: Self, url: URL) -> dict: ...


class ClickUseCaseImpl(ClickUseCaseProtocol):
    def __init__(self: Self, repository: ClickRepositoryProtocol):
        self.repository = repository

    async def log_click(self: Self, url_id: int):
        await self.repository.add_click(url_id=url_id)

    async def get_stats(self: Self, url: URL):
        now = datetime.now(UTC)
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)

        last_hour_clicks = await self.repository.get_list_click(
            url_id=url.id, since=last_hour
        )
        last_day_clicks = await self.repository.get_list_click(
            url_id=url.id, since=last_day
        )

        return {
            "link": f"{settings.BASE_URL}/{url.code}",
            "original_link": url.original_url,
            "last_hour_clicks": last_hour_clicks,
            "last_day_clicks": last_day_clicks,
        }
