from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from starlette.responses import RedirectResponse

from src.clicks.domain.entity import Click
from src.dependencies import URLUseCase, ClickUseCase
from src.urls.delivery.dto import (
    CreateShortURLRequest,
    ShortURLResponse,
    FilterParamsShortURLsRequest,
    CreateShortURLResponse,
)
from src.users.auth.dependencies import get_current_user

router = APIRouter()


@router.post(
    "/url/",
    response_model=CreateShortURLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(
    url_in: CreateShortURLRequest,
    url_use_case: URLUseCase,
    user=Depends(get_current_user),
):
    """Создание новой короткой ссылки"""
    ...
    url = url_in.to_entity(user_id=user.id)
    result = await url_use_case.create_short_url(url=url)
    return CreateShortURLResponse(url=result)


@router.get(
    "/urls/", response_model=list[ShortURLResponse], status_code=status.HTTP_200_OK
)
async def user_list_short_urls(
    url_use_case: URLUseCase,
    user=Depends(get_current_user),
    filter_query: FilterParamsShortURLsRequest = Depends(),
):
    """Получение списка ссылок пользователя"""
    urls = await url_use_case.get_url_list_by_user_id(
        user_id=user.id, params=filter_query
    )
    return [ShortURLResponse.from_entity(url) for url in urls]


@router.get(
    "/url/{url_id}/", response_model=ShortURLResponse, status_code=status.HTTP_200_OK
)
async def get_url_info(
    url_id: int,
    url_use_case: URLUseCase,
    user=Depends(get_current_user),
):
    """Получение информации о конкретной ссылке"""
    url = await url_use_case.get_url_by_id(id=url_id, user_id=user.id)
    return ShortURLResponse.from_entity(url)


@router.patch(
    "/url/{url_id}/deactivate/",
    response_model=ShortURLResponse,
    status_code=status.HTTP_200_OK,
)
async def deactivate_short_url(
    url_id: int,
    url_use_case: URLUseCase,
    user=Depends(get_current_user),
):
    """Деактивировать короткую ссылку"""
    url = await url_use_case.deactivate_short_url_by_id(id=url_id, user_id=user.id)
    return ShortURLResponse.from_entity(url)


@router.get("/{code}/")
async def redirect_to_original(
    code: str,
    url_use_case: URLUseCase,
    click_use_case: ClickUseCase,
):
    """Редирект на оригинальную страницу"""
    url = await url_use_case.get_valid_weblink_by_alias(alias=code)
    await click_use_case.log_click(Click(url_id=url.id))
    return RedirectResponse(url=url.original_url)


# @router.get(
#     "/{code}/resolve/",
#     response_model=CreateShortURLResponse,
#     status_code=status.HTTP_302_FOUND,
# )
# async def redirect_to_original_test(
#     code: str,
#     url_use_case: URLUseCase,
# ):
#     """Проверить правильно ли работает редирект (swagger UI не может редиректить)"""
#     original = await url_use_case.get_original_valid_url(code)
#     return CreateShortURLResponse(url=original)
