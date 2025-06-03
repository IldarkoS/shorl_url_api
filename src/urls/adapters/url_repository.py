from typing import Self

from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.urls.adapters.model import URL as URLModel
from src.urls.domain.entity import URL as URLEntity, QueryParams
from src.urls.domain.entity import UrlRepoProtocol


class UrlRepoImpl(UrlRepoProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _orm_to_entity(orm: URLModel):
        return URLEntity(
            id=orm.id,
            original_url=orm.original_url,
            code=orm.code,
            created_at=orm.created_at,
            expires_at=orm.expires_at,
            is_active=orm.is_active,
            user_id=orm.user_id,
        )
        # return URLEntity.model_validate(orm, from_attributes=True)

    @staticmethod
    def _entity_to_orm(entity: URLEntity):
        return URLModel(
            original_url=entity.original_url,
            expires_at=entity.expires_at,
            code=entity.code,
            is_active=entity.is_active,
            user_id=entity.user_id,
        )
        # return URLModel(**entity.model_dump(exclude_none=True, exclude=("id", "created_at")))

    async def create_url(self: Self, url: URLEntity) -> URLEntity:
        orm = self._entity_to_orm(url)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return self._orm_to_entity(orm)

    async def get_url_by_id(self: Self, id: int) -> URLEntity | None:
        stmt = select(URLModel).where(URLModel.id == id)
        result: Result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._orm_to_entity(orm) if orm else None

    async def get_url_by_alias(self: Self, alias: str) -> URLEntity | None:
        stmt = select(URLModel).where(URLModel.code == alias)
        result: Result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._orm_to_entity(orm) if orm else None

    async def get_urls_by_user_id(
        self: Self, user_id: int, params: QueryParams
    ) -> list[URLEntity]:
        stmt = select(URLModel).where(URLModel.user_id == user_id)
        if params.is_active is not None:
            stmt = stmt.where(URLModel.is_active == params.is_active)
        stmt = stmt.offset(params.offset).limit(params.limit)

        result: Result = await self.session.execute(stmt)
        orms = result.scalars().all()
        return [self._orm_to_entity(orm) for orm in orms]

    async def deactivate_url_by_id(self: Self, id: int) -> URLEntity | None:
        stmt = (
            update(URLModel)
            .where(URLModel.id == id)
            .values(is_active=False)
            .returning(URLModel)
        )
        result: Result = await self.session.execute(stmt)
        await self.session.commit()
        orm = result.scalar_one_or_none()
        return self._orm_to_entity(orm) if orm else None
