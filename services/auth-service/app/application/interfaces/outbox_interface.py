from abc import abstractmethod
from typing import Protocol

from app.domain.entities.message_entity import Message


class OutboxSaver(Protocol):
    @abstractmethod
    async def save(self, message: Message) -> None:
        ...


class OutboxReader(Protocol):
    @abstractmethod
    async def read_all(self) -> list[Message]:
        ...


class OutboxUpdater(Protocol):
    @abstractmethod
    async def update(self, id: int, update_data: dict) -> Message | None:
        ...
