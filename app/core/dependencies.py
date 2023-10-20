from typing import Any, Generator, Dict
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.database.db import SessionLocal
from app.database.models.user import User


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/api/auth/login')


def get_db() -> Generator:
    with SessionLocal() as session:
        yield session


def auth_security(token: str = Depends(OAUTH2_SCHEME)) -> str:
    return token


class CurrentUser:
    _instance = None

    def __init__(self):
        self.token: str = None
        self.user: User = None

    def __new__(cls, *args, **kwargs):  # Implements Singleton
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
