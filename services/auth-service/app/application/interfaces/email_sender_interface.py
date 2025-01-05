from abc import abstractmethod
from typing import Protocol


class EmailSender(Protocol):
    @abstractmethod
    async def send_email(self, recipient: str, subject: str, body: str) -> None:
        ...
