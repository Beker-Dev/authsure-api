from .base import RepositoryBase
from app.database.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(RepositoryBase[User, UserCreate, UserUpdate]):
    pass


user_repository = UserRepository(User)
