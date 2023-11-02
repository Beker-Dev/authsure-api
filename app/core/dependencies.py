from typing import Any, Generator, Dict
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.database.models.user import User
from app.utils.authentication.jwt import JWT
from app.repository.session import session_repository
from app.repository.user import user_repository
from app.schemas.user import CurrentUser


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/api/auth/login')


def get_db() -> Generator:
    with SessionLocal() as session:
        yield session


def auth_security(token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)) -> CurrentUser:
    try:
        JWT().jwt_token_validator(token)
        session = session_repository.get_by(db, {'token': token})
        if not session or not session.is_active:
            raise Exception
        else:
            user = user_repository.get(db, id=session.user_id)
            return CurrentUser(token=token, user=user)
    except:
        raise HTTPException(status_code=401, detail='Invalid token')


# class CurrentUser:
#     _instance = None
#
#     def __init__(self):
#         self.token: str = None
#         self.user: User = None
#
#     def __new__(cls, *args, **kwargs):  # Implements Singleton
#         if not isinstance(cls._instance, cls):
#             cls._instance = object.__new__(cls, *args, **kwargs)
#         return cls._instance
