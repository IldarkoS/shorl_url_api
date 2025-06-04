from typing import Self

from src.core.exceptions import UserAlreadyExists, InvalidCredentials
from src.users.adapters.user_repository import UserRepoProtocol
from src.users.auth.auth import password_hash, verify_password, create_access_token
from src.users.domain.entity import User
from src.users.domain.entity import UserUseCaseProtocol, PlainUser


class UserUseCaseImpl(UserUseCaseProtocol):
    def __init__(self, repository: UserRepoProtocol):
        self.repository = repository

    async def register_user(self: Self, creds: PlainUser) -> User:
        exists = await self.repository.get_user_by_username(username=creds.username)
        if exists:
            raise UserAlreadyExists("Username already taken")
        hashed_password = password_hash(creds.plain_password)
        user = User(username=creds.username, hashed_password=hashed_password)
        user = await self.repository.create_user(user=user)
        return user

    async def login_user(self: Self, creds: PlainUser) -> str:
        user = await self.repository.get_user_by_username(username=creds.username)
        if not user or not verify_password(creds.plain_password, user.hashed_password):
            raise InvalidCredentials("Invalid credentials")
        return create_access_token({"sub": str(user.id)})
