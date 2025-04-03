from fastapi import APIRouter, Security

from app.common.auth.depend import authenticate_api_key
from app.common.session import SessionDep
from app.dto.user_dto import UserLoginRequest, UserLoginResponse
from app.service.user_service import user_login_service, user_register_service
from app.common.auth.jwt_tool import generate_jwt
from app.common.log import log


router = APIRouter(dependencies=[Security(authenticate_api_key)])

@router.post("/login", response_model=UserLoginResponse)
async def login_user(
    session: SessionDep,
    login_data: UserLoginRequest
):
    user = user_login_service(session, login_data.name, login_data.password)

    log.info(f"user login: {user.name}")
    return UserLoginResponse(
        id=user.id,
        name=user.name,
        token=generate_jwt(user.id),
        last_login=user.last_login
    )


@router.post("/register", response_model=UserLoginResponse)
async def register_user(
    session: SessionDep,
    login_data: UserLoginRequest
):
    user = user_register_service(session, login_data.name, login_data.password)

    log.info(f"user register: {user.name}")
    return UserLoginResponse(
        id=user.id,
        name=user.name,
        token=generate_jwt(user.id),
        last_login=user.last_login
    )


# @router.get("/chat")
# async def chat_user():
#     message = '现在几点了'
    
#     log.info(f"user: {message}")
    
#     async def generate():
#         response_text = ""
#         for content in dashscope_client.chat_completion(message):
#             response_text += content
#             yield content
#         log.info(f"assistant: {response_text}")
    
#     return StreamingResponse(generate(), media_type="text/plain")