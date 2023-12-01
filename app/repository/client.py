from .base import RepositoryBase
from app.database.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from app.schemas.authentication import AuthenticationClientLogin
from app.utils.repository_utils.get_repository import get_repository_by_name

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


class ClientRepository(RepositoryBase[Client, ClientCreate, ClientUpdate]):
    def find_by_authentication_client_login(self, db: Session, client: AuthenticationClientLogin) -> Client:
        if db_client := db.query(Client).filter(Client.key == client.key, Client.secret == client.secret).first():
            return db_client
        raise HTTPException(401, "Invalid client credentials")

    def create(self, db: Session, obj_in: ClientCreate) -> Client:
        role_repository = get_repository_by_name("role", "role_repository")
        roles = [role_repository.get(db, role_id) for role_id in obj_in.roles]
        obj_in.roles = roles
        return super().create_with_association(db, obj_in)

    def update(self, db: Session, db_obj: User, obj_in: ClientUpdate) -> Client:
        role_repository = get_repository_by_name("role", "role_repository")
        roles = [role_repository.get(db, role_id) for role_id in obj_in.roles]
        obj_in.roles = roles
        custom_obj_data = jsonable_encoder(db_obj)
        custom_obj_data["roles"] = jsonable_encoder(db_obj.roles)
        return super().update(db, db_obj, obj_in, custom_obj_data)


client_repository = ClientRepository(Client)
