from abc import abstractmethod
from typing import Protocol

from app.domain.entities.user_entity import User


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None:
        ...


class UserReader(Protocol):
    @abstractmethod
    async def read_by_email(self, email: str) -> User | None:
        ...


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, email: str, update_data: dict) -> User | None:
        ...
