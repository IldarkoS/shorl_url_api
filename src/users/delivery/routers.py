from fastapi import APIRouter, HTTPException, status, Response
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
    try:
        user = await user_use_case.register_user(register_in.username, register_in.password)
        return RegisterUserResponse.model_validate(user, from_attributes=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login/", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_user(
    login_in: LoginRequest,
    response: Response,
    user_use_case: UserUseCase,
):
    try:
        token = await user_use_case.login_user(login_in.username, login_in.password)
        response.set_cookie("access_token", token, httponly=True)
        return LoginResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/logout/", status_code=status.HTTP_200_OK)
async def logout_user(response: Response) -> JSONResponse:
    response.delete_cookie("access_token")
    return JSONResponse({"Success": "Logged out!"})
