from datetime import datetime
from typing import Self, Protocol

from pydantic import BaseModel

from src.urls.domain.entity import URL


class Click(BaseModel):
    id: int | None = None
    url_id: int
    timestamp: datetime | None = None


class ClickRepositoryProtocol(Protocol):
    async def add_click(self: Self, click: Click) -> Click: ...

    async def get_list_click_by_url_id(self: Self, url_id: int, since: datetime) -> list[Click]: ...

class ClickUseCaseProtocol(Protocol):
    async def log_click(self: Self, click: Click) -> None: ...

    async def get_stats_by_url_id(self: Self, url: URL) -> dict: ...