from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.realm import realm_repository
from app.schemas.realm import RealmShow, RealmCreate, RealmUpdate
from app.core.dependencies import auth_security


class RealmRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Realms'], prefix='/realms', dependencies=[Depends(auth_security)])
        self.router.add_api_route("", self.show_realms, response_model=List[RealmShow], methods=["GET"])
        self.router.add_api_route("/{id}", self.show_realm, response_model=RealmShow, methods=["GET"])
        self.router.add_api_route("", self.create_realm, response_model=RealmShow, methods=["POST"])
        self.router.add_api_route("/{id}", self.update_realm, response_model=RealmShow, methods=["PUT"])
        self.router.add_api_route("/{id}", self.delete_realm, response_model=RealmShow, methods=["DELETE"])

    async def show_realms(self, db: Session = Depends(get_db)):
        return realm_repository.get_multi(db)

    async def show_realm(self, id: int, db: Session = Depends(get_db)):
        return realm_repository.get_or_404(db, id)

    async def create_realm(self, realm: RealmCreate, db: Session = Depends(get_db)):
        return realm_repository.create(db, obj_in=realm)

    async def update_realm(self, id: int, realm: RealmUpdate, db: Session = Depends(get_db)):
        db_realm = realm_repository.get_or_404(db, id)
        return realm_repository.update(db, db_obj=db_realm, obj_in=realm)

    async def delete_realm(self, id: int, db: Session = Depends(get_db)):
        db_realm = realm_repository.get_or_404(db, id)
        return realm_repository.remove(db, id=db_realm.id)


router = RealmRouter().router
