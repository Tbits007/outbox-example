from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from app.application.dtos.user_dtos import CreateUserDTO, LoginUserDTO
from app.application.exceptions.access import AuthenticationError
from app.application.exceptions.user import UserCannotBeCreatedError
from app.application.interactors import auth_interactors
from app.presentation.controllers.http.auth.schemas import request as request_schemas

auth_router = APIRouter()


@auth_router.post("/register")
@inject
async def register(
    data: request_schemas.RegisterRequest,
    interactor: FromDishka[auth_interactors.RegisterInteractor],
) -> dict[str, str]:
    try:
        dto = CreateUserDTO(
            email=str(data.email),
            username=data.username,
            password=data.password,
        )
        await interactor(dto)
        return {"message": "User created successfully"}
    except UserCannotBeCreatedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.reason,
        )


@auth_router.get("/verify-email")
@inject
async def verify(token: str, interactor: FromDishka[auth_interactors.VerifyInteractor]) -> dict[str, str]:
    try:
        await interactor(token)
        return {"message": "User verified successfully"}
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed")


@auth_router.post("/login")
@inject
async def login(
    data: request_schemas.LoginRequest,
    interactor: FromDishka[auth_interactors.LoginInteractor],
) -> dict[str, str]:
    try:
        dto = LoginUserDTO(email=str(data.email), password=data.password)
        tokens = await interactor(dto)
        return tokens
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed")


@auth_router.post("/password-reset")
@inject
async def password_reset(
    data: request_schemas.PasswordResetRequest,
    interactor: FromDishka[auth_interactors.PasswordResetInteractor],
) -> dict[str, str]:
    await interactor(str(data.email))
    return {"message": "Reset link was successfully sent"}


@auth_router.post("/password-reset-confirm")
@inject
async def password_reset_confirm(
    data: request_schemas.PasswordResetConfirmRequest,
    interactor: FromDishka[auth_interactors.PasswordResetConfirmInteractor],
) -> dict[str, str]:
    try:
        await interactor(data.token, data.new_password)
        return {"message": "New password has been successfully set"}
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed")
