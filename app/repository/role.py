from .base import RepositoryBase
from app.database.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


class RoleRepository(RepositoryBase[Role, RoleCreate, RoleUpdate]):
    pass


role_repository = RoleRepository(Role)
