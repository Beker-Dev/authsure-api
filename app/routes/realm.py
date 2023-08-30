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


@router.get("/{id}", response_model=RealmShow)
async def show_realm(id: int, db: Session = Depends(get_db)):
    return realm_repository.get_or_404(db, id)


@router.post("", response_model=RealmShow)
async def create_realm(realm: RealmCreate, db: Session = Depends(get_db)):
    return realm_repository.create(db, obj_in=realm)


@router.put("/{id}", response_model=RealmShow)
async def update_realm(id: int, realm: RealmUpdate, db: Session = Depends(get_db)):
    db_realm = realm_repository.get_or_404(db, id)
    return realm_repository.update(db, db_obj=db_realm, obj_in=realm)


@router.delete("/{id}", response_model=RealmShow)
async def delete_realm(id: int, db: Session = Depends(get_db)):
    db_realm = realm_repository.get_or_404(db, id)
    return realm_repository.remove(db, id=db_realm.id)
