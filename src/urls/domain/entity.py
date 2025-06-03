from datetime import datetime
from typing import Protocol, Self

from pydantic import BaseModel, Field


class URL(BaseModel):
    id: int | None = None
    original_url: str
    code: str | None = None
    created_at: datetime | None = None
    expires_at: datetime | None = None
    is_active: bool = True
    user_id: int


class QueryParams(BaseModel):
    is_active: bool | None = None
    offset: int = 0
    limit: int = Field(20, ge=1, le=100)


class UrlRepoProtocol(Protocol):
    async def create_url(self: Self, url: URL) -> URL: ...

    async def get_url_by_id(self: Self, id: int) -> URL | None: ...

    async def get_url_by_alias(self: Self, alias: str) -> URL | None: ...

    async def get_urls_by_user_id(
        self: Self, user_id: int, params: QueryParams
    ) -> list[URL]: ...

    async def deactivate_url_by_id(self: Self, id: int) -> URL | None: ...


class URLUseCaseProtocol(Protocol):
    async def create_short_url(self: Self, url: URL) -> str: ...

    async def deactivate_short_url_by_id(self: Self, id: int, user_id: int) -> URL: ...

    async def get_url_by_id(self: Self, id: int, user_id: int) -> URL: ...

    async def get_url_list_by_user_id(
        self: Self, user_id: int, params: QueryParams
    ) -> list[URL]: ...

    async def get_valid_weblink_by_alias(self: Self, alias: str) -> URL: ...
