from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


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

    def update(self, db: Session, db_obj: User, obj_in: RoleUpdate) -> Role:
        client_repository = get_repository_by_name("client", "client_repository")
        clients = [client_repository.get(db, client_id) for client_id in obj_in.clients]
        obj_in.clients = clients
        custom_obj_data = jsonable_encoder(db_obj)
        custom_obj_data["clients"] = jsonable_encoder(db_obj.clients)
        return super().update(db, db_obj, obj_in, custom_obj_data)


role_repository = RoleRepository(Role)
