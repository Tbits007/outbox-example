from abc import abstractmethod
from enum import Enum
from typing import Protocol


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    PASSWORD_RESET = "password_reset"
    ACCOUNT_VERIFICATION = "account_verification"


class JwtTokenProcessor(Protocol):
    @abstractmethod
    def create_access_token(self, user_email: str) -> str:
        ...

    @abstractmethod
    def create_password_reset_token(self, user_email: str) -> str:
        ...

    @abstractmethod
    def create_refresh_token(self, user_email: str) -> str:
        ...

    @abstractmethod
    def verify_token(self, token: str, token_type: TokenType | None = None) -> str | None:
        ...
