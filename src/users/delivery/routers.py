from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse

from src.dependencies import UserUseCase
from src.users.delivery.dto import (
    LoginResponse,
    RegisterUserResponse,
    RegisterUserRequest,
    LoginRequest,
)

router = APIRouter()


@router.post("/register/", response_model=RegisterUserResponse, status_code=201)
async def register_user(
    register_in: RegisterUserRequest,
    user_use_case: UserUseCase,
):
    """Регистрация пользователя"""
    plain_user = register_in.to_entity()
    user = await user_use_case.register_user(plain_user)
    return RegisterUserResponse.model_validate(user, from_attributes=True)


@router.post("/login/", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_user(
    login_in: LoginRequest,
    response: Response,
    user_use_case: UserUseCase,
):
    """Аутентификация пользователя"""
    plain_user = login_in.to_entity()
    token = await user_use_case.login_user(plain_user)
    response.set_cookie("access_token", token, httponly=True)
    return LoginResponse(access_token=token)


@router.post("/logout/", status_code=status.HTTP_200_OK)
async def logout_user(response: Response) -> JSONResponse:
    """Выход пользователя"""
    response.delete_cookie("access_token")
    return JSONResponse({"Success": "Logged out!"})
