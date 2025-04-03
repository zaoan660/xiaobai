from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.common.config import conf
from app.common.session import SessionDep
import jwt
from app.common.auth.jwt_tool import ALGORITHM
from app.common import errors
from sqlmodel import select
from app.model import User

auth_scheme = HTTPBearer()


async def authenticate_api_key(
    db_session: SessionDep,
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    authenticate_value = "Bearer"
    input_token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    if not input_token:
        raise credentials_exception
    
    try:
        # timestamp check is included in jwt.decode
        data = jwt.decode(
            input_token, conf.JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
    # InvalidTokenError是ExpiredSignatureError的超类
    except jwt.exceptions.ExpiredSignatureError:
        raise errors.TokenExpired("Token expired")
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception
    
    user_id = data.get("user_id")
    
    user = db_session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise errors.NotFoundError("用户不存在")
    
    return user
