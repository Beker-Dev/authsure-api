from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.database.models.user import User
from app.database.models.client import Client
from app.utils.repository_utils.filters import FilterJoin, Filter
from app.repository.user import user_repository
from app.repository.client import client_repository
from app.repository.role import role_repository
from app.repository.group import group_repository


def check_permissions(user: User, client: Client) -> bool:
    user_roles = [role.name for role in user.roles]
    user_group_roles = [role.name for group in user.groups for role in group.roles]
    permissions = user_roles + user_group_roles

    if client.name in permissions:
        return True
    raise HTTPException(403, "User does not have permission to access this client")
