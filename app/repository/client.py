from .base import RepositoryBase
from app.database.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientRepository(RepositoryBase[Client, ClientCreate, ClientUpdate]):
    pass


client_repository = ClientRepository(Client)
