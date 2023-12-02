from fastapi import HTTPException

from app.database.models.user import User
from app.database.models.client import Client


def check_permissions(user: User, client: Client) -> bool:
    user_roles = [role for role in user.roles]
    user_group_roles = [role for group in user.groups for role in group.roles]
    user_permissions = user_roles + user_group_roles

    for role in client.roles:
        if role in user_permissions:
            return True
    raise HTTPException(403, "User does not have permission to access this client")
