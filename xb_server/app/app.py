from fastapi import FastAPI, Request
from app.common.client.dashscope_client import dashscope_client
from fastapi.responses import StreamingResponse
from app.common import log, conf
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_pagination import add_pagination
from fastapi.responses import RedirectResponse
from app.common import errors
from fastapi.exceptions import RequestValidationError
from app.common.exception_handler import notify_exception, server_base_exception_handler, request_validation_exception_handler
from app.view.user_view import router as user_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.add_exception_handler(errors.ServerBaseError, server_base_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, notify_exception)

app.include_router(user_router, prefix="/user")


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return RedirectResponse(url="/redoc")