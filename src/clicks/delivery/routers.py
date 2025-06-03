from fastapi import APIRouter, Depends

from src.clicks.delivery.dto import ClickStatsResponse
from src.dependencies import URLUseCase, ClickUseCase
from src.users.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/urls/{url_id}/stats/", response_model=ClickStatsResponse)
async def get_url_stats(
    url_id: int,
    url_use_case: URLUseCase,
    click_use_case: ClickUseCase,
    user=Depends(get_current_user),
):
    """Просмотреть статистику переходов по ссылке"""
    url = await url_use_case.get_url(
        id=url_id,
        user_id=user.id,
    )
    return await click_use_case.get_stats(url=url)
