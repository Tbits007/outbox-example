from app.application.exceptions.base import ApplicationError


class AuthenticationError(ApplicationError):
    ...


class AccessDenied(ApplicationError):
    ...
