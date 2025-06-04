from datetime import datetime, UTC, timedelta
from typing import Self

from src.clicks.adapters.click_repository import ClickRepositoryProtocol
from src.clicks.domain.entity import ClickUseCaseProtocol, Click
from src.config import settings
from src.urls.adapters.model import URL


class ClickUseCaseImpl(ClickUseCaseProtocol):
    def __init__(self: Self, repository: ClickRepositoryProtocol):
        self.repository = repository

    async def log_click(self: Self, click: Click) -> None:
        await self.repository.add_click(click=click)

    async def get_stats(self: Self, url: URL) -> dict:
        now = datetime.now(UTC)
        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)

        last_hour_clicks = await self.repository.get_list_click_by_url_id(
            url_id=url.id, since=last_hour
        )
        last_day_clicks = await self.repository.get_list_click_by_url_id(
            url_id=url.id, since=last_day
        )

        return {
            "link": f"{settings.BASE_URL}/{url.code}",
            "original_link": url.original_url,
            "last_hour_clicks": len(last_hour_clicks),
            "last_day_clicks": len(last_day_clicks),
        }
