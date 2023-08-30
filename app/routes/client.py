from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.client import client_repository
from app.schemas.client import ClientShow, ClientCreate, ClientUpdate

router = APIRouter(tags=['Clients'], prefix='/clients')


@router.get("", response_model=List[ClientShow])
async def show_clients(db: Session = Depends(get_db)):
    return client_repository.get_multi(db)


@router.get("/{id}", response_model=ClientShow)
async def show_client(id: int, db: Session = Depends(get_db)):
    return client_repository.get_or_404(db, id)


@router.post("", response_model=ClientShow)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return client_repository.create(db, obj_in=client)


@router.put("/{id}", response_model=ClientShow)
async def update_client(id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = client_repository.get_or_404(db, id)
    return client_repository.update(db, db_obj=db_client, obj_in=client)


@router.delete("/{id}", response_model=ClientShow)
async def delete_client(id: int, db: Session = Depends(get_db)):
    db_client = client_repository.get_or_404(db, id)
    return client_repository.remove(db, id=db_client.id)
