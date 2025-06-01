from datetime import datetime
from typing import Protocol, Self

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.short_urls.domain.short_url import ShortURL


class ShortUrlRepoProtocol(Protocol):
    async def create_url(
        self: Self,
        original_url: str,
        short_url: str,
        user_id: int,
        expires_at: datetime = None,
    ) -> ShortURL: ...

    async def get_url_by_id(self: Self, id: int) -> ShortURL | None: ...

    async def get_url_by_code(self: Self, code: str) -> ShortURL | None: ...

    async def get_urls_by_user(
        self: Self, user_id: int, is_active: bool | None, offset: int, limit: int
    ) -> list[ShortURL]: ...

    async def deactivate_url(self: Self, id: int) -> ShortURL | None: ...


class ShortUrlRepoImpl(ShortUrlRepoProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_url(
        self: Self,
        original_url: str,
        short_url: str,
        user_id: int,
        expires_at: datetime = None,
    ) -> ShortURL:
        url = ShortURL(
            original_url=original_url,
            short_url=short_url,
            user_id=user_id,
            expires_at=expires_at,
        )
        self.session.add(url)
        await self.session.commit()
        return url

    async def get_url_by_id(self: Self, id: int) -> ShortURL | None:
        stmt = select(ShortURL).where(ShortURL.id == id)
        result: Result = await self.session.execute(stmt)
        url = result.scalar_one_or_none()
        return url

    async def get_url_by_code(self: Self, code: str) -> ShortURL | None:
        stmt = select(ShortURL).where(ShortURL.short_url == code)
        result: Result = await self.session.execute(stmt)
        url = result.scalar_one_or_none()
        return url

    async def get_urls_by_user(
        self: Self, user_id: int, is_active: bool | None, offset: int, limit: int
    ) -> list[ShortURL]:
        stmt = select(ShortURL).where(ShortURL.user_id == user_id)
        if is_active is not None:
            stmt.where(ShortURL.is_active == is_active)
        stmt = stmt.offset(offset).limit(limit)

        result: Result = await self.session.execute(stmt)
        urls = result.scalars().all()
        return list(urls)

    async def deactivate_url(self: Self, id: int) -> ShortURL | None:
        stmt = select(ShortURL).where(ShortURL.id == id)
        result: Result = await self.session.execute(stmt)
        url = result.scalar_one_or_none()
        if url:
            url.is_active = False
            await self.session.commit()
        return url
