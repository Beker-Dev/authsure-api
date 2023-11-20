from sqlalchemy.orm import Session

from app.database.models.user import User
from app.database.models.client import Client
from app.utils.repository_utils.filters import FilterJoin, Filter
from app.repository.user import user_repository
from app.repository.client import client_repository
from app.repository.role import role_repository
from app.repository.group import group_repository


def check_permissions(db: Session, user: User, client: Client) -> bool:
    print('groups', user.groups)
    print('roles', user.roles)
    # check user.roles / user.roles
    return True
