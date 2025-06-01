from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import db_helper
from src.users.adapters.user_repo_impl import UserRepoProtocol, UserRepoImpl
from src.users.usecases.user_use_case import UserUseCaseProtocol, UserUseCaseImpl

Session = Annotated[AsyncSession, Depends(db_helper.session_dependency)]

def get_user_repo(session: Session) -> UserRepoProtocol:
    return UserRepoImpl(session=session)

UserRepo = Annotated[UserRepoProtocol, Depends(get_user_repo)]

def get_user_use_case(user_repo: UserRepo) -> UserUseCaseProtocol:
    return UserUseCaseImpl(repo=user_repo)

UserUseCase = Annotated[UserUseCaseProtocol, Depends(get_user_use_case)]