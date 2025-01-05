from app.application.interfaces import user_interface
from app.application.interfaces.uow_interface import UnitOfWork
from app.domain.entities.user_entity import User


class GetUserInteractor:
    def __init__(
        self,
        user_gateway: user_interface.UserReader,
    ) -> None:
        self._user_gateway = user_gateway

    async def __call__(self, email: str) -> User | None:
        return await self._user_gateway.read_by_email(email)


class UpdateUserInteractor:
    def __init__(
        self,
        user_gateway: user_interface.UserUpdater,
        uow: UnitOfWork,
    ) -> None:
        self._user_gateway = user_gateway
        self._uow = uow

    async def __call__(self, email: str, update_data: dict) -> User | None:
        async with self._uow:
            user = await self._user_gateway.update(email, update_data)
            self._uow.commit()

        return user
