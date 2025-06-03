import random
from datetime import datetime, UTC
from typing import Self

from src.config import settings
from src.core.exceptions import (
    URLNotFound,
    URLAccessDenied,
    URLInactive,
    URLExpired,
    URLGenerationFailed,
)
from src.urls.domain.entity import QueryParams, URLUseCaseProtocol, UrlRepoProtocol, URL


class URLUseCaseImpl(URLUseCaseProtocol):
    def __init__(self: Self, repository: UrlRepoProtocol):
        self.repository = repository

    async def create_short_url(self: Self, url: URL) -> str:
        length: int = settings.SHORT_URL_LENGHT
        max_attempts: int = settings.MAX_GENERATION_ATTEMPTS
        alphabet: str = settings.ALPHABET
        base_url: str = settings.BASE_URL

        for _ in range(max_attempts):
            alias = self._generate_code(length=length, alphabet=alphabet)
            exists = await self.repository.get_url_by_alias(alias=alias)
            if not exists:
                url.code = alias
                result = await self.repository.create_url(url=url)
                return f"{base_url}/{result.code}/"

        raise URLGenerationFailed("Failed to generate short url, try again later!")

    async def deactivate_short_url_by_id(self: Self, id: int, user_id: int) -> URL:
        url = await self.repository.get_url_by_id(id=id)
        if not url:
            raise URLNotFound("URL not found")
        elif user_id != url.user_id:
            raise URLAccessDenied("URL not yours")
        elif not url.is_active:
            raise URLInactive("URL is already unactive")
        else:
            url = await self.repository.deactivate_url_by_id(id=id)
            return url

    async def get_url_by_id(self: Self, id: int, user_id: int) -> URL:
        url = await self.repository.get_url_by_id(id=id)
        if not url:
            raise URLNotFound("URL not found")
        elif user_id != url.user_id:
            raise URLAccessDenied("URL not yours")
        else:
            return url

    async def get_url_list_by_user_id(
        self: Self, user_id: int, params: QueryParams
    ) -> list[URL]:
        urls = await self.repository.get_urls_by_user_id(user_id=user_id, params=params)
        return urls

    async def get_valid_weblink_by_alias(self: Self, alias: str) -> URL:
        url = await self.repository.get_url_by_alias(alias=alias)
        if not url:
            raise URLNotFound("URL not found")
        elif not url.is_active:
            raise URLInactive("URL is already unactive")
        elif url.expires_at < datetime.now(UTC):
            raise URLExpired("ShortURL expired!")
        else:
            return url

    @staticmethod
    def _generate_code(length: int, alphabet: str) -> str:
        return "".join(random.choices(population=alphabet, k=length))
