from sqlalchemy.orm import Session

from .base import RepositoryBase
from app.database.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate
from app.utils.repository_utils.get_repository import get_repository_by_name


class RoleRepository(RepositoryBase[Role, RoleCreate, RoleUpdate]):
    def create(self, db: Session, obj_in: RoleCreate) -> Role:
        client_repository = get_repository_by_name("client", "client_repository")
        clients = [client_repository.get(db, client_id) for client_id in obj_in.clients]
        obj_in.clients = clients
        return super().create_with_association(db, obj_in)


role_repository = RoleRepository(Role)
