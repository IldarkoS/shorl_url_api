from typing import Protocol, Self

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.domain.user import User


class UserRepoProtocol(Protocol):
    async def create_user(self: Self, username: str, hashed_password: str) -> User: ...

    async def get_user_by_username(self: Self, username: str) -> User | None: ...

    async def get_user_by_id(self: Self, id: int) -> User | None: ...


class UserRepoImpl(UserRepoProtocol):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self: Self, username: str, hashed_password: str) -> User:
        new_user = User(
            username=username,
            hashed_password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_user_by_username(self: Self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self: Self, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        result: Result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
