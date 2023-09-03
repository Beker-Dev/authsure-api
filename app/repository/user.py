from sqlalchemy.orm import Session

from .base import RepositoryBase
from app.database.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(RepositoryBase[User, UserCreate, UserUpdate]):
    def update_password(self, db: Session, db_obj: User, password: str) -> User:
        db_obj.password = password

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user_repository = UserRepository(User)
