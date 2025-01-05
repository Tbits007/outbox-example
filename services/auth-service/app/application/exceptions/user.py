from app.application.exceptions.base import ApplicationError


class UserCannotBeCreatedError(ApplicationError):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class UserNotFoundError(ApplicationError):
    ...
