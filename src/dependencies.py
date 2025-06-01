from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import db_helper
from src.short_urls.adapters.short_url_repository import ShortUrlRepoProtocol, ShortUrlRepoImpl
from src.short_urls.usecases.urls_use_case import (
    ShortURLUseCaseProtocol,
    ShortURLUseCaseImpl,
)
from src.users.adapters.user_repository import UserRepoProtocol, UserRepoImpl
from src.users.usecases.user_use_case import UserUseCaseProtocol, UserUseCaseImpl

Session = Annotated[AsyncSession, Depends(db_helper.session_dependency)]

def get_user_repo(session: Session) -> UserRepoProtocol:
    return UserRepoImpl(session=session)

UserRepo = Annotated[UserRepoProtocol, Depends(get_user_repo)]

def get_user_use_case(user_repo: UserRepo) -> UserUseCaseProtocol:
    return UserUseCaseImpl(repo=user_repo)

UserUseCase = Annotated[UserUseCaseProtocol, Depends(get_user_use_case)]


def get_short_url_repo(session: Session) -> ShortUrlRepoProtocol:
    return ShortUrlRepoImpl(session=session)

ShortURLRepo = Annotated[ShortUrlRepoProtocol, Depends(get_short_url_repo)]

def get_short_url_use_case(repository: ShortURLRepo) -> ShortURLUseCaseProtocol:
    return ShortURLUseCaseImpl(repository=repository)

ShortURLUseCase = Annotated[ShortURLUseCaseProtocol, Depends(get_short_url_use_case)]