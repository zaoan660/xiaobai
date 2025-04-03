from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    DEBUG: bool = False
    # HTTP
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

    # AUTH
    JWT_SECRET_KEY: str

    # AI Token
    DASHSCOPE_API_KEY: str

    class Config:
        case_sensitive = True


current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(current_dir, "..", ".env"))

conf = Settings()
