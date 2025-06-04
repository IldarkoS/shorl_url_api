from typing import Protocol, Self

from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    username: str
    hashed_password: str


class PlainUser(BaseModel):
    id: int | None = None
    username: str
    plain_password: str


class UserRepoProtocol(Protocol):
    async def create_user(self: Self, user: User) -> User: ...

    async def get_user_by_username(self: Self, username: str) -> User | None: ...

    async def get_user_by_id(self: Self, id: int) -> User | None: ...


class UserUseCaseProtocol(Protocol):
    async def register_user(self: Self, creds: PlainUser) -> User: ...

    async def login_user(self: Self, creds: PlainUser) -> str: ...
