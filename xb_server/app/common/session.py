from sqlmodel import Session, create_engine
from app.common import conf
from typing import Annotated
from fastapi import Depends

DATABASE_URI = f"mysql+pymysql://{conf.MYSQL_USER}:{conf.MYSQL_PASSWORD}@{conf.MYSQL_HOST}:{conf.MYSQL_PORT}/{conf.MYSQL_DB}"
engine = create_engine(DATABASE_URI)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]