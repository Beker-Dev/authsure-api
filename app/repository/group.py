from .base import RepositoryBase
from app.database.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate
from app.schemas.user import UserShow
from app.repository.user import user_repository
from app.schemas.role import RoleShow
from app.repository.role import role_repository

from sqlalchemy.orm import Session


class GroupRepository(RepositoryBase[Group, GroupCreate, GroupUpdate]):
    def create(self, db: Session, obj_in: GroupCreate) -> Group:
        users = [user_repository.get(db, user_id) for user_id in obj_in.users]
        roles = [role_repository.get(db, role_id) for role_id in obj_in.roles]
        obj_in.users = users
        obj_in.roles = roles
        print('object', obj_in)
        return super().create_with_association(db, obj_in)


group_repository = GroupRepository(Group)
