from sqlalchemy.orm import Session
from fastapi import HTTPException

from .base import RepositoryBase
from app.database.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.authentication import AuthenticationLogin
from app.utils.hash_utils import Password
from app.utils.repository_utils.get_repository import get_repository_by_name


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

    def create(self, db: Session, obj_in: UserCreate) -> User:
        group_repository = get_repository_by_name("group", "group_repository")
        role_repository = get_repository_by_name("role", "role_repository")
        groups = [group_repository.get(db, group_id) for group_id in obj_in.groups]
        roles = [role_repository.get(db, role_id) for role_id in obj_in.roles]
        obj_in.groups = groups
        obj_in.roles = roles
        return super().create_with_association(db, obj_in)


user_repository = UserRepository(User)
