from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    PasswordMismatchError,
    UserNotFoundError,
    WeakPasswordError,
    OrganizationAlreadyExistsError,
    OrganizationNotFoundError,
    UnauthorizedOrganizationAccessError,
    UserAlreadyInOrganizationError,
    WorkspaceNotFoundError,
    WorkspaceAlreadyExistsError,
    DocumentNotFoundError,
    DocumentAlreadyExistsError,
    InvalidDocumentError,
    UnsupportedDocumentTypeError,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(EmailAlreadyExistsError)
    async def email_exists_handler(
        request: Request,
        exc: EmailAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(InvalidRefreshTokenError)
    async def invalid_refresh_handler(
        request: Request,
        exc: InvalidRefreshTokenError,
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "error": {
                    "code": "INVALID_REFRESH_TOKEN",
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(PasswordMismatchError)
    async def password_mismatch_handler(
        request: Request,
        exc: PasswordMismatchError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": {
                    "code": "PASSWORD_MISMATCH",
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(WeakPasswordError)
    async def weak_password_handler(
        request: Request,
        exc: WeakPasswordError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": {
                    "code": "WEAK_PASSWORD",
                    "message": exc.message,
                },
            },
        )


    import traceback
    from app.core.logging import logger

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
        return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Something went wrong."
            },
        },
    ) 
    @app.exception_handler(OrganizationAlreadyExistsError)
    async def organization_already_exists_handler(
        request: Request,
        exc: OrganizationAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": {
                    "code": "ORGANIZATION_ALREADY_EXISTS",
                    "message": exc.message,
                },
            },
        )
    @app.exception_handler(OrganizationNotFoundError)
    async def organization_not_found_handler(
        request: Request,
        exc: OrganizationNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "code": "ORGANIZATION_NOT_FOUND",
                    "message": exc.message,
                },
            },
        )
    @app.exception_handler(UnauthorizedOrganizationAccessError)
    async def unauthorized_organization_access_handler(
        request: Request,
        exc: UnauthorizedOrganizationAccessError,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "success": False,
                "error": {
                    "code": "UNAUTHORIZED_ORGANIZATION_ACCESS",
                    "message": exc.message,
                },
            },
        )
    @app.exception_handler(UserAlreadyInOrganizationError)
    async def user_already_in_organization_handler(
        request: Request,
        exc: UserAlreadyInOrganizationError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": {
                    "code": "USER_ALREADY_IN_ORGANIZATION",
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(WorkspaceNotFoundError)
    async def workspace_not_found_handler(
        request: Request,
        exc: WorkspaceNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "code": "WORKSPACE_NOT_FOUND",
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(DocumentNotFoundError)
    async def document_not_found_handler(
        request: Request,
        exc: DocumentNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": {
                    "code": "DOCUMENT_NOT_FOUND",
                    "message": str(exc),
                },
            },
        )

    @app.exception_handler(DocumentAlreadyExistsError)
    async def document_already_exists_handler(
        request: Request,
        exc: DocumentAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": {
                    "code": "DOCUMENT_ALREADY_EXISTS",
                    "message": str(exc),
                },
            },
        )

    @app.exception_handler(WorkspaceAlreadyExistsError)
    async def workspace_already_exists_handler(
        request: Request,
        exc: WorkspaceAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": {
                    "code": "WORKSPACE_ALREADY_EXISTS",
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(InvalidDocumentError)
    async def invalid_document_handler(
        request: Request,
        exc: InvalidDocumentError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": {
                    "code": "INVALID_DOCUMENT",
                    "message": str(exc),
                },
            },
        )

    @app.exception_handler(UnsupportedDocumentTypeError)
    async def unsupported_document_type_handler(
        request: Request,
        exc: UnsupportedDocumentTypeError,
    ):
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={
                "success": False,
                "error": {
                    "code": "UNSUPPORTED_DOCUMENT_TYPE",
                    "message": str(exc),
                },
            },
        )