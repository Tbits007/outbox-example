from dataclasses import dataclass


@dataclass(slots=True)
class Action:
    email: str
    action_type: str
    details: str | None = None

    _id: str | None = None
