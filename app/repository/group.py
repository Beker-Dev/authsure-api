from .base import RepositoryBase
from app.database.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate


class GroupRepository(RepositoryBase[Group, GroupCreate, GroupUpdate]):
    pass


group_repository = GroupRepository(Group)
