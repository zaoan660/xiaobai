from sqlmodel import Field, SQLModel
import time
import uuid
from sqlalchemy import Column, String, DateTime
import base62
from datetime import datetime

def gen_base62_uuid():
    my_uuid = uuid.uuid4()
    base62_uuid = base62.encode(int(my_uuid))
    return base62_uuid


def gen_id(prefix=None):
    if prefix:
        return f"{prefix}_{gen_base62_uuid()}"
    else:
        return gen_base62_uuid()
    

class User(SQLModel, table=True):
    __tablename__ = "xb_user"
    id: str = Field(sa_column=Column(String(255), primary_key=True), default_factory=lambda: "xbu_" + gen_id())
    name: str = Field(sa_column=Column(String(255), nullable=False))
    password: str = Field(sa_column=Column(String(255), nullable=False))
    created_at: datetime = Field(sa_column=Column(DateTime, nullable=False), default_factory=lambda: datetime.now())
    last_login: datetime = Field(sa_column=Column(DateTime, nullable=False), default_factory=lambda: datetime.now())



