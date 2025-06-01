from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.db import db_helper
from src.users.adapters.user_repository import UserRepoImpl


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token), session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    try:
        payload = jwt.decode(token, key=settings.AUTH_JWT.SECRET_KEY, algorithms=settings.AUTH_JWT.ALGORITHM)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    repo = UserRepoImpl(session)
    user = await repo.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
