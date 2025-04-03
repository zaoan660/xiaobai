from app.common import errors
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.exceptions import RequestValidationError
from app.common.log import log
from fastapi.encoders import jsonable_encoder


def notify_exception(request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )


async def request_validation_exception_handler(request, exc: RequestValidationError):
    log.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 40000,
            "message": "Validation Error",
            "detail": jsonable_encoder(exc.errors()),
        },
    )


async def server_base_exception_handler(request, exc: errors.ServerBaseError):
    log.error(f"Server base error: {status.HTTP_400_BAD_REQUEST} {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": exc.code, "message": exc.message},
    )
