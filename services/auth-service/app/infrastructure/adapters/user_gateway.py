from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions.user import UserCannotBeCreatedError, UserNotFoundError
from app.application.interfaces.user_interface import UserReader, UserSaver, UserUpdater
from app.domain.entities.user_entity import User
from app.infrastructure.data_access.models.user_model import DBUser


class UserGateway(UserReader, UserSaver, UserUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User) -> None:
        query = select(DBUser).where(DBUser.email == user.email)
        existing_user = await self._session.execute(query)
        existing_user = existing_user.scalar_one_or_none()

        if existing_user:
            raise UserCannotBeCreatedError(f"User with email {user.email} already exists")

        db_user = DBUser(
            email=user.email,
            username=user.username,
            password=user.password,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
        )
        self._session.add(db_user)

    async def read_by_email(self, email: str) -> User | None:
        query = select(DBUser).where(DBUser.email == email)
        result = await self._session.execute(query)
        db_user = result.scalar_one()
        if not db_user:
            raise UserNotFoundError

        return User(
            email=db_user.email,
            username=db_user.username,
            password=db_user.password,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            is_superuser=db_user.is_superuser,
        )

    async def update(self, email: str, update_data: dict) -> User | None:
        query = select(DBUser).where(DBUser.email == email)
        result = await self._session.execute(query)
        db_user = result.scalar_one()
        if not db_user:
            raise UserNotFoundError

        for field, value in update_data.items():
            if hasattr(db_user, field):
                setattr(db_user, field, value)

        return User(
            email=db_user.email,
            username=db_user.username,
            password=db_user.password,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            is_superuser=db_user.is_superuser,
        )
