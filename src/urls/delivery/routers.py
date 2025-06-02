from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from starlette.responses import RedirectResponse

from src.dependencies import URLUseCase
from src.urls.delivery.dto import (
    CreateShortURLRequest,
    ShortURLResponse,
    FilterParamsShortURLsRequest,
    CreateShortURLResponse,
)
from src.users.auth.dependencies import get_current_user

router = APIRouter()


@router.post(
    "/create/",
    response_model=CreateShortURLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(
    short_url_in: CreateShortURLRequest,
    url_use_case: URLUseCase,
    user=Depends(get_current_user),
):
    result = await url_use_case.create_short_url(
        original_url=str(short_url_in.original_url),
        user_id=user.id,
        expires_at=short_url_in.expires_at,
    )
    return CreateShortURLResponse(url=result)


@router.get(
    "/list/", response_model=list[ShortURLResponse], status_code=status.HTTP_200_OK
)
async def user_list_short_urls(
    url_use_case: URLUseCase,
    user=Depends(get_current_user),
    filter_query: FilterParamsShortURLsRequest = Depends(),
):
    result = await url_use_case.get_urls_list(
        user_id=user.id,
        offset=filter_query.offset,
        limit=filter_query.limit,
        is_active=filter_query.is_active,
    )
    return result


@router.get(
    "/list/{url_id}/", response_model=ShortURLResponse, status_code=status.HTTP_200_OK
)
async def get_url_info(
    url_id: int,
    url_use_case: URLUseCase,
    user=Depends(get_current_user),
):
    result = await url_use_case.get_url(
        id=url_id,
        user_id=user.id,
    )
    return result


@router.patch(
    "/list/{url_id}/deactivate/",
    response_model=ShortURLResponse,
    status_code=status.HTTP_200_OK,
)
async def deactivate_short_url(
    url_id: int,
    url_use_case: URLUseCase,
    user=Depends(get_current_user),
):
    result = await url_use_case.deactivate_short_url(
        id=url_id,
        user_id=user.id,
    )
    return result


@router.get("/{code}/")
async def redirect_to_original(
    code: str,
    url_use_case: URLUseCase,
):
    """Редирект на оригинальную страницу"""
    original = await url_use_case.get_original_url(code)
    return RedirectResponse(url=original)


@router.get(
    "/{code}/resolve/",
    response_model=CreateShortURLResponse,
    status_code=status.HTTP_302_FOUND,
)
async def redirect_to_original(
    code: str,
    url_use_case: URLUseCase,
):
    """Проверить работает, ли правильно редирект (swagger UI не может редиректить)"""
    original = await url_use_case.get_original_url(code)
    return CreateShortURLResponse(url=original)
