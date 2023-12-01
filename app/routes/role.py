from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repository.role import role_repository
from app.schemas.role import RoleShow, RoleCreate, RoleUpdate, RoleShowPaginated
from app.core.dependencies import auth_security, permissions_security
from app.core.config import settings
from app.utils.filters.query_filters import DefaultFilter
from app.utils.repository_utils.filters import FilterJoin
from app.database.models.role import Role
from app.database.models.realm import Realm
from app.database.enums.role_type import RoleType


class RoleRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Roles'], prefix='/roles', dependencies=[Depends(auth_security)])
        self.router.add_api_route(
            '',
            self.show_roles,
            response_model=RoleShowPaginated,
            methods=['GET'],
            dependencies=[Depends(permissions_security(RoleType.role_view))]
        )
        self.router.add_api_route(
            '/{id}',
            self.show_role,
            response_model=RoleShow,
            methods=['GET'],
            dependencies=[Depends(permissions_security(RoleType.role_view))]
        )
        self.router.add_api_route(
            '',
            self.create_role,
            response_model=RoleShow,
            methods=['POST'],
            dependencies=[Depends(permissions_security(RoleType.role_create))]
        )
        self.router.add_api_route(
            '/{id}',
            self.update_role,
            response_model=RoleShow,
            methods=['PUT'],
            dependencies=[Depends(permissions_security(RoleType.role_update))]
        )
        self.router.add_api_route(
            '/{id}',
            self.delete_role,
            response_model=RoleShow,
            methods=['DELETE'],
            dependencies=[Depends(permissions_security(RoleType.role_delete))]
        )

    async def show_roles(
            self,
            query: DefaultFilter = Depends(DefaultFilter),
            db: Session = Depends(get_db),
            page: int = 1,
            c: int = settings.DEFAULT_PAGE_SIZE
    ) -> RoleShowPaginated:
        filters = [FilterJoin(Realm, Realm.id, Role.realm_id, [query.realm], 'name')]
        result_query = role_repository.get_by_join(db, filters_join=filters, skip=(page - 1) * c, limit=c)
        last_page_query = role_repository.get_by_join(db, filters_join=filters)
        roles = result_query.all()
        last_page = role_repository.get_last_page(last_page_query, c)
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
