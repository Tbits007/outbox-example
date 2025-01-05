from dataclasses import dataclass


@dataclass(slots=True)
class CreateActionDTO:
    email: str
    action_type: str
    details: str | None = None
