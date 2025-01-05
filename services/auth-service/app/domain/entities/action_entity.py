from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    USER_CREATED = "User created"
    USER_UPDATED = "User updated"


@dataclass(slots=True)
class ActionSchema:
    email: str
    action_type: ActionType
    details: str | None = None
