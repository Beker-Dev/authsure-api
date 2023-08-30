from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.realm import realm_repository
from app.schemas.realm import RealmShow, RealmCreate, RealmUpdate


router = APIRouter(tags=['Realms'], prefix='/realms')


@router.get("", response_model=List[RealmShow])
async def show_realms(db: Session = Depends(get_db)):
    return realm_repository.get_multi(db)
