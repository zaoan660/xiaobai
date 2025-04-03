from app.common import errors
from app.common.session import SessionDep
from app.model import User

from sqlmodel import select

from datetime import datetime

# 用户登录服务
def user_login_service(session: SessionDep, name: str, password: str) -> User:
    user = session.exec(select(User).where(User.name == name)).first()
    if not user or user.password != password:
        raise errors.UserLoginError()

    # 更新最后登录时间
    user.last_login = datetime.now()
    session.commit()
    return user


# 用户注册服务
def user_register_service(session: SessionDep, name: str, password: str) -> User:
    # 检查用户名是否已存在
    existing_user = session.exec(select(User).where(User.name == name)).first()
    if existing_user:
        raise errors.AlreadyExistError("用户名已存在")
    
    # 创建新用户
    new_user = User(
        name=name,
        password=password,
        last_login=datetime.now()
    )
    
    # 添加到数据库
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user
