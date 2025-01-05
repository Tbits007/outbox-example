from fastapi import HTTPException, Request

from app.application.exceptions.access import AuthenticationError
from app.application.interfaces.email_provider_interface import EmailProvider
from app.application.interfaces.jwt_processor_interface import JwtTokenProcessor, TokenType


class SimpleEmailProvider(EmailProvider):
    def __init__(self, jwt_token_processor: JwtTokenProcessor) -> None:
        self._jwt_token_processor = jwt_token_processor

    def __call__(self, request: Request) -> str | None:
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            email = self._jwt_token_processor.verify_token(
                token=authorization.split("Bearer ")[1],
                token_type=TokenType.ACCESS,
            )
            return email
        except AuthenticationError:
            raise HTTPException(status_code=401, detail="Unauthorized")
