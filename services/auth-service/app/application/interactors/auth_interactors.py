import json
from dataclasses import asdict

from app.application.dtos.user_dtos import CreateUserDTO, LoginUserDTO
from app.application.exceptions.access import AuthenticationError
from app.application.interfaces.email_sender_interface import EmailSender
from app.application.interfaces.jwt_processor_interface import JwtTokenProcessor, TokenType
from app.application.interfaces.link_creator_interface import LinkCreator
from app.application.interfaces.outbox_interface import OutboxSaver
from app.application.interfaces.password_hasher_interface import PasswordHasher
from app.application.interfaces.uow_interface import UnitOfWork
from app.application.interfaces.user_interface import UserReader, UserSaver, UserUpdater
from app.domain.entities.action_entity import ActionSchema, ActionType
from app.domain.entities.message_entity import Message
from app.domain.entities.user_entity import User


class RegisterInteractor:
    def __init__(
        self,
        user_gateway: UserSaver,
        outbox_gateway: OutboxSaver,
        email_sender: EmailSender,
        link_creator: LinkCreator,
        jwt_token_processor: JwtTokenProcessor,
        password_hasher: PasswordHasher,
        uow: UnitOfWork,
    ) -> None:
        self._user_gateway = user_gateway
        self._outbox_gateway = outbox_gateway
        self._email_sender = email_sender
        self._link_creator = link_creator
        self._jwt_token_processor = jwt_token_processor
        self._password_hasher = password_hasher
        self._uow = uow

    async def __call__(self, dto: CreateUserDTO) -> None:
        async with self._uow:
            hashed_password = self._password_hasher.get_password_hash(dto.password)
            user = User(
                email=dto.email,
                username=dto.username,
                password=hashed_password,
            )
            await self._user_gateway.save(user)

            token = self._jwt_token_processor.create_access_token(dto.email)
            verification_link = self._link_creator.create_verification_link(token)
            await self._email_sender.send_email(
                recipient=dto.email,
                subject="Account verification",
                body=f"Hi {dto.username}, visit the link: {verification_link} to verify account",
            )

            action = ActionSchema(
                email=dto.email,
                action_type=ActionType.USER_CREATED.value,
                details=f"User {dto.email} created successfully",
            )
            payload = json.dumps(asdict(action))
            message = Message(payload=payload)
            await self._outbox_gateway.save(message)

            await self._uow.commit()


class VerifyInteractor:
    def __init__(
        self,
        user_gateway: UserUpdater,
        jwt_token_processor: JwtTokenProcessor,
        uow: UnitOfWork,
    ) -> None:
        self._user_gateway = user_gateway
        self._jwt_token_processor = jwt_token_processor
        self._uow = uow

    async def __call__(self, token: str) -> None:
        async with self._uow:
            email = self._jwt_token_processor.verify_token(token, token_type=TokenType.ACCESS)
            await self._user_gateway.update(email, {"is_verified": True})
            await self._uow.commit()


class LoginInteractor:
    def __init__(
        self,
        user_gateway: UserReader,
        password_hasher: PasswordHasher,
        jwt_token_processor: JwtTokenProcessor,
    ) -> None:
        self._user_gateway = user_gateway
        self._password_hasher = password_hasher
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, dto: LoginUserDTO) -> dict:
        user = await self._user_gateway.read_by_email(dto.email)
        if not user or not self._password_hasher.verify_password(dto.password, user.password):
            raise AuthenticationError
        if not user.is_verified:
            raise AuthenticationError

        access_token = self._jwt_token_processor.create_access_token(user.email)
        refresh_token = self._jwt_token_processor.create_refresh_token(user.email)
        return {"access_token": access_token, "refresh_token": refresh_token}


class PasswordResetInteractor:
    def __init__(
        self,
        user_gateway: UserReader,
        email_gateway: EmailSender,
        link_creator: LinkCreator,
        jwt_token_processor: JwtTokenProcessor,
    ) -> None:
        self._user_gateway = user_gateway
        self._email_gateway = email_gateway
        self._link_creator = link_creator
        self._jwt_token_processor = jwt_token_processor

    async def __call__(self, email: str) -> None:
        user = await self._user_gateway.read_by_email(email)
        if user:
            token = self._jwt_token_processor.create_password_reset_token(email)
            reset_link = self._link_creator.create_password_reset_link(token)
            await self._email_gateway.send_email(
                recipient=email,
                subject="Password Reset",
                body=f"Hi, visit the link: {reset_link} to reset your password.",
            )


class PasswordResetConfirmInteractor:
    def __init__(
        self,
        user_gateway: UserUpdater,
        password_hasher: PasswordHasher,
        jwt_token_processor: JwtTokenProcessor,
        uow: UnitOfWork,
    ):
        self._user_gateway = user_gateway
        self._password_hasher = password_hasher
        self._jwt_token_processor = jwt_token_processor
        self._uow = uow

    async def __call__(self, token: str, password: str) -> None:
        async with self._uow:
            email = self._jwt_token_processor.verify_token(token, token_type=TokenType.PASSWORD_RESET)
            hashed_password = self._password_hasher.get_password_hash(password)
            await self._user_gateway.update(email, {"password": hashed_password})
            await self._uow.commit()
