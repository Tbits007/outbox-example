from datetime import datetime, timedelta, timezone
from typing import Literal

from jose import JWTError, jwt

from app.application.exceptions.access import AuthenticationError
from app.application.interfaces.jwt_processor_interface import JwtTokenProcessor, TokenType
from app.main.config import Config

Algorithm = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
]


class SimpleJwtTokenProcessor(JwtTokenProcessor):
    def __init__(self, config: Config) -> None:
        self.secret = config.jwt_.SECRET_KEY
        self.access_token_expires = config.jwt_.ACCESS_TOKEN_EXPIRES_MINUTES
        self.refresh_token_expires = config.jwt_.REFRESH_TOKEN_EXPIRES_MINUTES
        self.algorithm = config.jwt_.ALGORITHM

    def create_access_token(self, user_email: str) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + timedelta(minutes=self.access_token_expires)
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": user_email,
            "type": TokenType.ACCESS.value,
        }
        return jwt.encode(
            to_encode,
            self.secret,
            algorithm=self.algorithm,
        )

    def create_password_reset_token(self, user_email: str) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + timedelta(minutes=self.access_token_expires)
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": user_email,
            "type": TokenType.PASSWORD_RESET.value,
        }
        return jwt.encode(
            to_encode,
            self.secret,
            algorithm=self.algorithm,
        )

    def create_refresh_token(self, user_email: str) -> str:
        issued_at = datetime.now(timezone.utc)
        expires = issued_at + timedelta(minutes=self.refresh_token_expires)
        to_encode = {
            "exp": expires,
            "iat": issued_at,
            "sub": user_email,
            "type": TokenType.REFRESH.value,
        }
        return jwt.encode(
            to_encode,
            self.secret,
            algorithm=self.algorithm,
        )

    def verify_token(self, token: str, token_type: TokenType | None = None) -> str | None:
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
            )
            if token_type and payload.get("type") != token_type.value:
                raise AuthenticationError("Invalid token type")
            return payload["sub"]
        except JWTError:
            raise AuthenticationError
