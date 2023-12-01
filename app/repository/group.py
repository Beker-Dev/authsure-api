from .base import RepositoryBase
from app.database.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate
from app.utils.repository_utils.get_repository import get_repository_by_name

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


class GroupRepository(RepositoryBase[Group, GroupCreate, GroupUpdate]):
    def create(self, db: Session, obj_in: GroupCreate) -> Group:
        user_repository = get_repository_by_name("user", "user_repository")
        role_repository = get_repository_by_name("role", "role_repository")
        users = [user_repository.get(db, user_id) for user_id in obj_in.users]
        roles = [role_repository.get(db, role_id) for role_id in obj_in.roles]
        obj_in.users = users
        obj_in.roles = roles
        return super().create_with_association(db, obj_in)

    def update(self, db: Session, db_obj: User, obj_in: GroupUpdate) -> Group:
        user_repository = get_repository_by_name("user", "user_repository")
        role_repository = get_repository_by_name("role", "role_repository")
        users = [user_repository.get(db, user_id) for user_id in obj_in.users]
        roles = [role_repository.get(db, role_id) for role_id in obj_in.roles]
        obj_in.users = users
        obj_in.roles = roles
        custom_obj_data = jsonable_encoder(db_obj)
        custom_obj_data["users"] = jsonable_encoder(db_obj.users)
        custom_obj_data["roles"] = jsonable_encoder(db_obj.roles)
        return super().update(db, db_obj, obj_in, custom_obj_data)


group_repository = GroupRepository(Group)
