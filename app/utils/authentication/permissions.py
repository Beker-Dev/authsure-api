from fastapi import HTTPException

from app.database.models.user import User
from app.database.models.client import Client


def check_permissions(user: User, client: Client) -> bool:
    user_roles = [role.name for role in user.roles]
    user_group_roles = [role.name for group in user.groups for role in group.roles]
    permissions = user_roles + user_group_roles

    if client.name in permissions:
        return True
    raise HTTPException(403, "User does not have permission to access this client")
