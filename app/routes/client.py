from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.client import client_repository
from app.schemas.client import ClientShow, ClientCreate, ClientUpdate
from app.core.dependencies import auth_security


class ClientRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Clients'], prefix='/clients', dependencies=[Depends(auth_security)])
        self.router.add_api_route("", self.show_clients, response_model=List[ClientShow], methods=["GET"])
        self.router.add_api_route("/{id}", self.show_client, response_model=ClientShow, methods=["GET"])
        self.router.add_api_route("", self.create_client, response_model=ClientShow, methods=["POST"])
        self.router.add_api_route("/{id}", self.update_client, response_model=ClientShow, methods=["PUT"])
        self.router.add_api_route("/{id}", self.delete_client, response_model=ClientShow, methods=["DELETE"])

    async def show_clients(self, db: Session = Depends(get_db)):
        return client_repository.get_multi(db)

    async def show_client(self, id: int, db: Session = Depends(get_db)):
        return client_repository.get_or_404(db, id)

    async def create_client(self, client: ClientCreate, db: Session = Depends(get_db)):
        return client_repository.create(db, obj_in=client)

    async def update_client(self, id: int, client: ClientUpdate, db: Session = Depends(get_db)):
        db_client = client_repository.get_or_404(db, id)
        return client_repository.update(db, db_obj=db_client, obj_in=client)

    async def delete_client(self, id: int, db: Session = Depends(get_db)):
        db_client = client_repository.get_or_404(db, id)
        return client_repository.remove(db, id=db_client.id)


router = ClientRouter().router
