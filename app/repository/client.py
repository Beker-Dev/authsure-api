from .base import RepositoryBase
from app.database.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from app.schemas.authentication import AuthenticationClientLogin

from fastapi import HTTPException
from sqlalchemy.orm import Session


class ClientRepository(RepositoryBase[Client, ClientCreate, ClientUpdate]):
    def find_by_authentication_client_login(self, db: Session, client: AuthenticationClientLogin) -> Client:
        if db_client := db.query(Client).filter(Client.key == client.key, Client.secret == client.secret).first():
            return db_client
        raise HTTPException(401, "Invalid client credentials")


client_repository = ClientRepository(Client)
