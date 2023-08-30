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
