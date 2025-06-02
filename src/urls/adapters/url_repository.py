from datetime import datetime
from typing import Protocol, Self

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.urls.domain.url import URL


class ShortUrlRepoProtocol(Protocol):
    async def create_url(
        self: Self,
        original_url: str,
        code: str,
        user_id: int,
        expires_at: datetime = None,
    ) -> URL: ...

    async def get_url_by_id(self: Self, id: int) -> URL | None: ...

    async def get_url_by_code(self: Self, code: str) -> URL | None: ...

    async def get_urls_by_user(
        self: Self, user_id: int, is_active: bool | None, offset: int, limit: int
    ) -> list[URL]: ...

    async def deactivate_url(self: Self, id: int) -> URL | None: ...


class ShortUrlRepoImpl(ShortUrlRepoProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_url(
        self: Self,
        original_url: str,
        code: str,
        user_id: int,
        expires_at: datetime = None,
    ) -> URL:
        url = URL(
            original_url=original_url,
            code=code,
            user_id=user_id,
            expires_at=expires_at,
        )
        self.session.add(url)
        await self.session.commit()
        return url

    async def get_url_by_id(self: Self, id: int) -> URL | None:
        stmt = select(URL).where(URL.id == id)
        result: Result = await self.session.execute(stmt)
        url = result.scalar_one_or_none()
        return url

    async def get_url_by_code(self: Self, code: str) -> URL | None:
        stmt = select(URL).where(URL.code == code)
        result: Result = await self.session.execute(stmt)
        url = result.scalar_one_or_none()
        return url

    async def get_urls_by_user(
        self: Self, user_id: int, is_active: bool | None, offset: int, limit: int
    ) -> list[URL]:
        stmt = select(URL).where(URL.user_id == user_id)
        if is_active is not None:
            stmt = stmt.where(URL.is_active == is_active)
        stmt = stmt.offset(offset).limit(limit)

        result: Result = await self.session.execute(stmt)
        urls = result.scalars().all()
        return list(urls)

    async def deactivate_url(self: Self, id: int) -> URL | None:
        stmt = select(URL).where(URL.id == id)
        result: Result = await self.session.execute(stmt)
        url = result.scalar_one_or_none()
        if url:
            url.is_active = False
            await self.session.commit()
        return url
