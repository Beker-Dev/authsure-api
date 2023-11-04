from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.role import role_repository
from app.schemas.role import RoleShow, RoleCreate, RoleUpdate, RoleShowPaginated
from app.core.dependencies import auth_security
from app.core.config import settings


class RoleRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Roles'], prefix='/roles', dependencies=[Depends(auth_security)])
        self.router.add_api_route('', self.show_roles, response_model=RoleShowPaginated, methods=['GET'])
        self.router.add_api_route('/{id}', self.show_role, response_model=RoleShow, methods=['GET'])
        self.router.add_api_route('', self.create_role, response_model=RoleShow, methods=['POST'])
        self.router.add_api_route('/{id}', self.update_role, response_model=RoleShow, methods=['PUT'])
        self.router.add_api_route('/{id}', self.delete_role, response_model=RoleShow, methods=['DELETE'])

    async def show_roles(
            self,
            db: Session = Depends(get_db),
            page: int = 1,
            c: int = settings.DEFAULT_PAGE_SIZE
    ) -> RoleShowPaginated:
        roles = role_repository.get_multi(db, skip=(page - 1) * c, limit=c)
        last_page = role_repository.get_last_page(db, c)
        return RoleShowPaginated(
            roles=[RoleShow.model_validate(role) for role in roles],
            last_page=last_page,
            current_page=page,
            per_page=c
        )

    async def show_role(self, id: int, db: Session = Depends(get_db)) -> RoleShow:
        return role_repository.get_or_404(db, id)

    async def create_role(self, role: RoleCreate, db: Session = Depends(get_db)) -> RoleShow:
        return role_repository.create(db, obj_in=role)

    async def update_role(self, id: int, role: RoleUpdate, db: Session = Depends(get_db)) -> RoleShow:
        db_role = role_repository.get_or_404(db, id)
        return role_repository.update(db, db_obj=db_role, obj_in=role)

    async def delete_role(self, id: int, db: Session = Depends(get_db)) -> RoleShow:
        db_role = role_repository.get_or_404(db, id)
        return role_repository.remove(db, id=db_role.id)


router = RoleRouter().router
