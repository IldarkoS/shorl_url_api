from typing import Self

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.adapters.model import User as UserModel
from src.users.domain.entity import User as UserEntity, UserRepoProtocol


class UserRepoImpl(UserRepoProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _orm_to_entity(orm: UserModel):
        return UserEntity(
            id=orm.id,
            username=orm.username,
            hashed_password=orm.hashed_password,
        )

    @staticmethod
    def _entity_to_orm(entity: UserEntity):
        return UserModel(
            id=entity.id,
            username=entity.username,
            hashed_password=entity.hashed_password,
        )

    async def create_user(self: Self, user: UserEntity) -> UserEntity:
        orm = self._entity_to_orm(user)
        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)
        return self._orm_to_entity(orm)

    async def get_user_by_username(self: Self, username: str) -> UserEntity | None:
        stmt = select(UserModel).where(UserModel.username == username)
        result: Result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return self._orm_to_entity(user) if user else None

    async def get_user_by_id(self: Self, id: int) -> UserEntity | None:
        stmt = select(UserModel).where(UserModel.id == id)
        result: Result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return self._orm_to_entity(user) if user else None
