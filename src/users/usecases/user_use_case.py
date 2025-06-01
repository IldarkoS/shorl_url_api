from typing import Protocol, Self

from src.users.adapters.user_repository import UserRepoProtocol
from src.users.auth.auth import password_hash, verify_password, create_access_token
from src.users.domain.user import User


class UserUseCaseProtocol(Protocol):
    async def register_user(self: Self, username: str, password: str) -> User:
        ...

    async def login_user(self: Self, username: str, password: str) -> str:
        ...


class UserUseCaseImpl(UserUseCaseProtocol):
    def __init__(self, repo: UserRepoProtocol):
        self.repo = repo

    async def register_user(self: Self, username: str, password: str) -> User:
        existing_user = await self.repo.get_user_by_username(username=username)
        if existing_user:
            raise ValueError("Username already exists!")

        hashed_password = password_hash(password=password)
        user = await self.repo.create_user(username, hashed_password)
        return user

    async def login_user(self: Self, username: str, password: str) -> str:
        user = await self.repo.get_user_by_username(username=username)
        if not user or not verify_password(plain_password=password, hashed_password=user.hashed_password):
            raise ValueError('Invalid credentials')

        return create_access_token({
            "sub": str(user.id),
        })