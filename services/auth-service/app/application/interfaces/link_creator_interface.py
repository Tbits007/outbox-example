from abc import abstractmethod
from typing import Protocol


class LinkCreator(Protocol):
    @abstractmethod
    def create_verification_link(self, token: str) -> str:
        ...

    @abstractmethod
    def create_password_reset_link(self, token: str) -> str:
        ...
