import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from app.common.threading_storage import user_id_var, job_id_var

# Configuration
LOG_DIR = os.path.join(os.path.expanduser("~"), ".xiaobai")
LEVEL = logging.INFO
# Create directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)
formatter = logging.Formatter(
    "%(asctime)s [%(user_id)s,%(job_id)s] %(levelname)s [%(shortpath)s:%(lineno)d]  %(message)s",
    datefmt="%m-%d %H:%M:%S",
)


class ThreadLocalFilter(logging.Filter):
    def filter(self, record):
        record.user_id = user_id_var.get("-")
        record.job_id = job_id_var.get("-")

        # 获取最后一级目录加文件名
        full_path = record.pathname
        record.shortpath = os.path.sep.join(
            full_path.split(os.path.sep)[-2:]
        )  # 最后一级目录加文件名
        return True


# class ContextVarLogHandler(logging.Handler):
#     def emit(self, record):
#         log_entry = self.format(record)
#         # 获取当前请求的日志缓冲区
#         log_buffer = log_buffer_var.get([])
#         # 添加新的日志条目
#         log_buffer.append(log_entry)
#         # # 更新日志缓冲区
#         # log_buffer_var.set(log_buffer)


def create_logger(name, console=True, file=True, monitor=True):
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)
    logger.propagate = (
        False  # Prevent the log messages from being duplicated in the python console
    )
    # if monitor:
    #     log_handler = ContextVarLogHandler()
    #     log_handler.addFilter(ThreadLocalFilter())
    #     log_handler.setFormatter(formatter)
    #     logger.addHandler(log_handler)
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.addFilter(ThreadLocalFilter())
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if file:
        log_file_path = os.path.join(LOG_DIR, f"{name}.log")
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=1024 * 1024 * 5,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.addFilter(ThreadLocalFilter())
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


log = create_logger("server")
