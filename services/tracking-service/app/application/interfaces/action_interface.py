from abc import abstractmethod
from typing import Protocol

from app.domain.entities.action_entity import Action


class ActionSaver(Protocol):
    @abstractmethod
    async def save(self, action: Action) -> Action | None:
        ...


class ActionReader(Protocol):
    @abstractmethod
    async def read_by_id(self, _id: str) -> Action | None:
        ...
