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

class OrganizationAlreadyExistsError(AppException):
    pass

class OrganizationNotFoundError(AppException):
    pass

class UnauthorizedOrganizationAccessError(AppException):
    pass

class UserAlreadyInOrganizationError(AppException):
    pass

class WorkspaceAlreadyExistsError(AppException):
    status_code = 409
    error_code = "WORKSPACE_ALREADY_EXISTS"


class WorkspaceNotFoundError(AppException):
    status_code = 404
    error_code = "WORKSPACE_NOT_FOUND"


class DocumentNotFoundError(Exception):
    """Raised when a document cannot be found."""


class InvalidDocumentError(Exception):
    """Raised when an uploaded document is invalid."""


class UnsupportedDocumentTypeError(Exception):
    """Raised when file type is unsupported."""


class DocumentAlreadyExistsError(Exception):
    """Raised when duplicate document exists."""