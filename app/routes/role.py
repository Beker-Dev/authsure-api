from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.role import role_repository
from app.schemas.role import RoleShow, RoleCreate, RoleUpdate
from app.core.dependencies import auth_security


class RoleRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Roles'], prefix='/roles', dependencies=[Depends(auth_security)])
        self.router.add_api_route('', self.show_roles, response_model=List[RoleShow], methods=['GET'])
        self.router.add_api_route('/{id}', self.show_role, response_model=RoleShow, methods=['GET'])
        self.router.add_api_route('', self.create_role, response_model=RoleShow, methods=['POST'])
        self.router.add_api_route('/{id}', self.update_role, response_model=RoleShow, methods=['PUT'])
        self.router.add_api_route('/{id}', self.delete_role, response_model=RoleShow, methods=['DELETE'])

    async def show_roles(self, db: Session = Depends(get_db)):
        return role_repository.get_multi(db)

    async def show_role(self, id: int, db: Session = Depends(get_db)):
        return role_repository.get_or_404(db, id)

    async def create_role(self, role: RoleCreate, db: Session = Depends(get_db)):
        return role_repository.create(db, obj_in=role)

    async def update_role(self, id: int, role: RoleUpdate, db: Session = Depends(get_db)):
        db_role = role_repository.get_or_404(db, id)
        return role_repository.update(db, db_obj=db_role, obj_in=role)

    async def delete_role(self, id: int, db: Session = Depends(get_db)):
        db_role = role_repository.get_or_404(db, id)
        return role_repository.remove(db, id=db_role.id)


router = RoleRouter().router
