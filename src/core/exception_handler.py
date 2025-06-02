from fastapi import status, FastAPI
from fastapi.responses import JSONResponse

from src.core.exceptions import *


def setup_exception_handler(app: FastAPI) -> None:

    # URLs
    app.add_exception_handler(
        URLNotFound,
        lambda r, e: JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(e)},
        ),
    )

    app.add_exception_handler(
        URLAccessDenied,
        lambda r, e: JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(e)},
        ),
    )

    app.add_exception_handler(
        URLInactive,
        lambda r, e: JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(e)},
        ),
    )

    app.add_exception_handler(
        URLExpired,
        lambda r, e: JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(e)},
        ),
    )

    app.add_exception_handler(
        URLGenerationFailed,
        lambda r, e: JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)},
        ),
    )

    # Users
    app.add_exception_handler(
        UserAlreadyExists,
        lambda r, e: JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(e)},
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        lambda r, e: JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(e)},
        ),
    )
