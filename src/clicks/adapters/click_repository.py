from asyncio import Protocol
from datetime import datetime
from typing import Self

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.clicks.adapters.model import Click as ClickModel
from src.clicks.domain.entity import Click as ClickEntity
from src.clicks.domain.entity import ClickRepositoryProtocol


class ClickRepositoryImpl(ClickRepositoryProtocol):
    def __init__(self: Self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _orm_to_entity(orm: ClickModel):
        return ClickEntity(
            id=orm.id,
            timestamp=orm.timestamp,
            url_id=orm.url_id,
        )

    @staticmethod
    def _entity_to_orm(entity: ClickEntity):
        return ClickModel(
            timestamp=entity.timestamp,
            url_id=entity.url_id,
        )

    async def add_click(self: Self, click: ClickEntity) -> ClickEntity:
        orm = self._entity_to_orm(click)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return self._orm_to_entity(orm)

    async def get_list_click_by_url_id(self: Self, url_id: int, since: datetime) -> list[ClickEntity]:
        stmt = select(ClickModel).where(ClickModel.url_id == url_id, ClickModel.timestamp >= since)
        result: Result = await self.session.execute(stmt)
        orms = result.scalars().all()
        return [self._orm_to_entity(orm) for orm in orms]