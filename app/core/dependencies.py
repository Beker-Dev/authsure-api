from typing import Generator, List
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.utils.authentication.jwt import JWT
from app.repository.session import session_repository
from app.repository.user import user_repository
from app.schemas.user import CurrentUser
from app.database.enums.role_type import RoleType
from app.core.config import settings


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/api/auth/login')


def get_db() -> Generator:
    with SessionLocal() as session:
        yield session


def auth_security(token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)) -> CurrentUser:
    try:
        JWT(
            access_expires_minutes=settings.ACCESS_TOKEN_LIFETIME,
            refresh_expires_minutes=settings.REFRESH_TOKEN_LIFETIME
        ).jwt_token_validator(token)
        session = session_repository.get_by(db, {'token': token})
        if not session or not session.is_active:
            raise Exception
        else:
            user = user_repository.get(db, id=session.user_id)
            return CurrentUser(token=token, user=user)
    except Exception as e:
        print('error auth security', type(e), e)
        raise HTTPException(status_code=401, detail='Invalid token')


def permissions_security(
        permission_name: RoleType,
) -> List[RoleType]:
    def wrapper(current_user: CurrentUser = Depends(auth_security)):
        user = current_user.user
        user_permissions = [role_type for role in user.roles for role_type in role.types]
        if RoleType.full_access in user_permissions or permission_name in user_permissions:
            return user_permissions
        raise HTTPException(403, f"User does not have permission to access. Missing: {permission_name}")
    return wrapper

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
