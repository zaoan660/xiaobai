class MyBaseError(Exception):
    code = 0
    message = "Base error"

    def __init__(self, message=None):
        super().__init__()
        if not message:
            message = self.message
        self.message = message

class UnknownError(MyBaseError):
    code = -1
    message = "服务器内部错误"


class ServerBaseError(MyBaseError):
    code = 1
    message = "客户端错误"

# 通用的异常 100-999
class UnauthorizedError(ServerBaseError):
    code = 100
    message = "您没有权限执行此操作"

class PayloadValidationError(ServerBaseError):
    code = 101
    message = "请求参数无效，请检查并重试"

class NotFoundError(ServerBaseError):
    code = 102
    message = "未找到"

class ExpiredError(ServerBaseError):
    code = 103
    message = "已过期"

class AlreadyExistError(ServerBaseError):
    code = 104
    message = "已存在"

class StartupFailedError(ServerBaseError):
    code = 105
    message = "启动失败"


class UserLoginError(ServerBaseError):
    code = 106
    message = "用户名或密码错误"

class TokenExpired(ServerBaseError):
    code = 107
    message = "Token expired"


