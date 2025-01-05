from passlib.context import CryptContext

from app.application.interfaces.password_hasher_interface import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    def __init__(self) -> None:
        self._pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)
