from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status
from starlette.responses import RedirectResponse

from src.dependencies import ShortURLUseCase
from src.urls.delivery.dto import CreateShortURLRequest, ShortURLResponse, FilterParamsShortURLsRequest, \
    CreateShortURLResponse
from src.users.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/create/", response_model=CreateShortURLResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    short_url_in: CreateShortURLRequest,
    short_url_use_case: ShortURLUseCase,
    user = Depends(get_current_user)
):
    try:
        result = await short_url_use_case.create_short_url(
            original_url=str(short_url_in.original_url),
            user_id=user.id,
            expires_at=short_url_in.expires_at,
        )
        return CreateShortURLResponse(url=result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/list/", response_model=list[ShortURLResponse], status_code=status.HTTP_200_OK)
async def user_list_short_urls(
    short_url_use_case: ShortURLUseCase,
    user = Depends(get_current_user),
    filter_query: FilterParamsShortURLsRequest = Depends(),
):
    result = await short_url_use_case.get_urls_list(
        user_id=user.id,
        offset=filter_query.offset,
        limit=filter_query.limit,
        is_active=filter_query.is_active,
    )
    return result

@router.get("/list/{url_id}/", response_model=ShortURLResponse, status_code=status.HTTP_200_OK)
async def get_url_info(
    url_id: int,
    short_url_use_case: ShortURLUseCase,
    user = Depends(get_current_user),
):
    try:
        result = await short_url_use_case.get_url(
            id=url_id,
            user_id=user.id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.patch("/list/{url_id}/deactivate/", response_model=ShortURLResponse, status_code=status.HTTP_200_OK)
async def deactivate_short_url(
        url_id: int,
        short_url_use_case: ShortURLUseCase,
        user = Depends(get_current_user),
):
    try:
        result = await short_url_use_case.deactivate_short_url(
            id=url_id,
            user_id=user.id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.get("/{short_code}/")
async def redirect_to_original(
    short_code: str,
    short_url_use_case: ShortURLUseCase,
):
    try:
        original = await short_url_use_case.get_original_url(short_code)
        return RedirectResponse(url=original)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))