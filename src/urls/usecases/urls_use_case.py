import random
from datetime import datetime, UTC
from typing import Protocol, Self

from src.config import settings
from src.core.exceptions import (
    URLNotFound,
    URLAccessDenied,
    URLInactive,
    URLExpired,
    URLGenerationFailed,
)
from src.urls.adapters.url_repository import ShortUrlRepoProtocol
from src.urls.domain.url import URL


class ShortURLUseCaseProtocol(Protocol):
    async def create_short_url(
        self: Self, original_url: str, user_id: int, expires_at: datetime = None
    ) -> str: ...

    async def deactivate_short_url(self: Self, id: int, user_id: int) -> URL: ...

    async def get_url(self: Self, id: int, user_id: int) -> URL: ...

    async def get_urls_list(
        self: Self, user_id: int, is_active: bool, offset: int = 0, limit: int = 20
    ) -> list[URL]: ...

    async def get_original_url(self: Self, short_url: str) -> str: ...


class ShortURLUseCaseImpl(ShortURLUseCaseProtocol):
    def __init__(self: Self, repository: ShortUrlRepoProtocol):
        self.repository = repository

    async def create_short_url(
        self: Self, original_url: str, user_id: int, expires_at: datetime = None
    ) -> str:
        code = await self._generate_code()
        result = await self.repository.create_url(
            original_url=original_url,
            code=code,
            user_id=user_id,
            expires_at=expires_at,
        )
        return f"{settings.BASE_URL}/{result.code}"

    async def _generate_code(self: Self):
        lenght = settings.SHORT_URL_LENGHT
        max_attempts = settings.MAX_GENERATION_ATTEMPTS
        alphabet = settings.ALPHABET

        for _ in range(max_attempts):
            code = "".join(random.choices(population=alphabet, k=lenght))
            exists = await self.repository.get_url_by_code(code=code)
            if not exists:
                return code

        raise URLGenerationFailed("Failed to generate short url, try again later!")

    async def deactivate_short_url(self: Self, id: int, user_id: int) -> URL:
        url = await self.repository.get_url_by_id(id=id)
        if not url:
            raise URLNotFound("Url not found!")
        elif user_id != url.user_id:
            raise URLAccessDenied("Url not yours!")
        elif not url.is_active:
            raise URLInactive("Url is already unactive!")
        else:
            url = await self.repository.deactivate_url(id=id)
            return url

    async def get_url(self: Self, id: int, user_id: int) -> URL:
        url = await self.repository.get_url_by_id(id=id)
        if not url:
            raise URLNotFound("Url not found!")
        elif user_id != url.user_id:
            raise URLAccessDenied("Url not yours!")
        else:
            return url

    async def get_urls_list(
        self: Self,
        user_id: int,
        is_active: bool | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[URL]:
        urls = await self.repository.get_urls_by_user(
            user_id=user_id,
            is_active=is_active,
            offset=offset,
            limit=limit,
        )
        return urls

    async def get_original_url(self: Self, short_url: str) -> str:
        url = await self.repository.get_url_by_code(code=short_url)
        if not url:
            raise URLNotFound("ShortURL not found!")
        elif not url.is_active:
            raise URLInactive("ShortURL not active!")
        elif url.expires_at < datetime.now(UTC):
            raise URLExpired("ShortURL expired!")
        else:
            return url.original_url
