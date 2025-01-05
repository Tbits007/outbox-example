from dataclasses import dataclass
from enum import Enum


class MessageStatus(Enum):
    PENDING = "pending"
    SENT = "sent"


@dataclass(slots=True)
class Message:
    payload: str
    status: MessageStatus = MessageStatus.PENDING.value

    id: int = None
