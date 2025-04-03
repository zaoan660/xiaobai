from datetime import datetime
from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    name: str
    password: str


class UserLoginResponse(BaseModel):
    id: str
    name: str
    token: str
    last_login: datetime