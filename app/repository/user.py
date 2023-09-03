from sqlalchemy.orm import Session
from fastapi import HTTPException

from .base import RepositoryBase
from app.database.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.authentication import AuthenticationLogin
from app.utils.hash_utils import Password


class UserRepository(RepositoryBase[User, UserCreate, UserUpdate]):
    def update_password(self, db: Session, db_obj: User, password: str) -> User:
        db_obj.password = password

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def find_by_authentication_login(self, db: Session, user: AuthenticationLogin) -> User:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not Password.check(user.password, db_user.password):
            raise HTTPException(401, "Invalid credentials")
        return db_user


user_repository = UserRepository(User)
