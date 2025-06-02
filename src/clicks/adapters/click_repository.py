from asyncio import Protocol
from datetime import datetime
from typing import Self, List

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.clicks.domain.click import Click


class ClickRepositoryProtocol(Protocol):
    async def add_click(self: Self, url_id: int) -> Click: ...

    async def get_list_click(
        self: Self, url_id: int, since: datetime
    ) -> int: ...


class ClickRepositoryImpl(ClickRepositoryProtocol):
    def __init__(self: Self, session: AsyncSession):
        self.session = session

    async def add_click(self: Self, url_id: int) -> Click:
        self.session.add(Click(url_id=url_id))
        await self.session.commit()

    async def get_list_click(self: Self, url_id: int, since: datetime) -> int:
        stmt = select(Click).where(Click.url_id == url_id, Click.timestamp >= since)
        result: Result = await self.session.execute(stmt)
        return len(result.scalars().all())
