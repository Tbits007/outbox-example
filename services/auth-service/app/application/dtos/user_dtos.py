from dataclasses import dataclass


@dataclass(slots=True)
class CreateUserDTO:
    email: str
    username: str
    password: str


@dataclass(slots=True)
class LoginUserDTO:
    email: str
    password: str
