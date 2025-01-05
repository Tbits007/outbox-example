from dishka import Provider, Scope, provide

from app.application.interactors.auth_interactors import (
    LoginInteractor,
    PasswordResetConfirmInteractor,
    PasswordResetInteractor,
    RegisterInteractor,
    VerifyInteractor,
)
from app.application.interfaces import jwt_processor_interface, password_hasher_interface
from app.infrastructure.adapters.jwt_processor import SimpleJwtTokenProcessor
from app.infrastructure.adapters.password_hasher import Argon2PasswordHasher


class AuthProvider(Provider):
    register_interactor = provide(RegisterInteractor, scope=Scope.REQUEST)
    verify_interactor = provide(VerifyInteractor, scope=Scope.REQUEST)
    login_interactor = provide(LoginInteractor, scope=Scope.REQUEST)
    password_reset_interactor = provide(PasswordResetInteractor, scope=Scope.REQUEST)
    password_reset_confirm_interactor = provide(PasswordResetConfirmInteractor, scope=Scope.REQUEST)

    password_hasher = provide(
        Argon2PasswordHasher,
        scope=Scope.REQUEST,
        provides=password_hasher_interface.PasswordHasher,
    )

    jwt_token_processor = provide(
        SimpleJwtTokenProcessor,
        scope=Scope.REQUEST,
        provides=jwt_processor_interface.JwtTokenProcessor,
    )
