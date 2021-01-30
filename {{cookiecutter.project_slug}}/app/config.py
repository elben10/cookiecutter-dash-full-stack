import os

from pydantic import BaseSettings


class Config(BaseSettings):
    SECRET_KEY: bytes = os.urandom(12)
    SQLALCHEMY_DATABASE_URI: str


config = Config()
