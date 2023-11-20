from .base import RepositoryBase
from app.database.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate
from app.utils.repository_utils.get_repository import get_repository_by_name

from sqlalchemy.orm import Session


class GroupRepository(RepositoryBase[Group, GroupCreate, GroupUpdate]):
    def create(self, db: Session, obj_in: GroupCreate) -> Group:
        user_repository = get_repository_by_name("user", "user_repository")
        role_repository = get_repository_by_name("role", "role_repository")
        users = [user_repository.get(db, user_id) for user_id in obj_in.users]
        roles = [role_repository.get(db, role_id) for role_id in obj_in.roles]
        obj_in.users = users
        obj_in.roles = roles
        return super().create_with_association(db, obj_in)


group_repository = GroupRepository(Group)
