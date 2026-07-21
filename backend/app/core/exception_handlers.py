from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    PasswordMismatchError,
    UserNotFoundError,
    WeakPasswordError,
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


    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
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