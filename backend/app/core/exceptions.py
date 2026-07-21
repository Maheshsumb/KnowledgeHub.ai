class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EmailAlreadyExistsError(AppException):
    pass


class InvalidCredentialsError(AppException):
    pass


class InvalidRefreshTokenError(AppException):
    pass


class PasswordMismatchError(AppException):
    pass


class UserNotFoundError(AppException):
    pass


class WeakPasswordError(AppException):
    pass