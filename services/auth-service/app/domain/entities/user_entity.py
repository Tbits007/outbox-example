from dataclasses import dataclass


@dataclass(slots=True)
class User:
    email: str
    username: str
    password: str
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False
