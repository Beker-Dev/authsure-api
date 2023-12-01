from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repository.client import client_repository
from app.schemas.client import ClientShow, ClientCreate, ClientUpdate, ClientShowPaginated
from app.core.dependencies import auth_security, permissions_security
from app.core.config import settings
from app.utils.filters.query_filters import DefaultFilter
from app.utils.repository_utils.filters import FilterJoin
from app.database.models.client import Client
from app.database.models.realm import Realm
from app.database.enums.role_type import RoleType


class ClientRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Clients'], prefix='/clients', dependencies=[Depends(auth_security)])
        self.router.add_api_route(
            "",
            self.show_clients,
            response_model=ClientShowPaginated,
            methods=["GET"],
            dependencies=[Depends(permissions_security(RoleType.client_view))]
        )
        self.router.add_api_route(
            "/{id}",
            self.show_client,
            response_model=ClientShow,
            methods=["GET"],
            dependencies=[Depends(permissions_security(RoleType.client_view))]
        )
        self.router.add_api_route(
            "",
            self.create_client,
            response_model=ClientShow,
            methods=["POST"],
            dependencies=[Depends(permissions_security(RoleType.client_create))]
        )
        self.router.add_api_route(
            "/{id}",
            self.update_client,
            response_model=ClientShow,
            methods=["PUT"],
            dependencies=[Depends(permissions_security(RoleType.client_update))]
        )
        self.router.add_api_route(
            "/{id}",
            self.delete_client,
            response_model=ClientShow,
            methods=["DELETE"],
            dependencies=[Depends(permissions_security(RoleType.client_delete))]
        )

    async def show_clients(
            self,
            query: DefaultFilter = Depends(DefaultFilter),
            db: Session = Depends(get_db),
            page: int = 1,
            c: int = settings.DEFAULT_PAGE_SIZE
    ) -> ClientShowPaginated:
        filters = [FilterJoin(Realm, Realm.id, Client.realm_id, [query.realm], 'name')]
        result_query = client_repository.get_by_join(db, filters_join=filters, skip=(page - 1) * c, limit=c)
        last_page_query = client_repository.get_by_join(db, filters_join=filters)
        clients = result_query.all()
        last_page = client_repository.get_last_page(last_page_query, c)
        return ClientShowPaginated(
            clients=[ClientShow.model_validate(client) for client in clients],
            last_page=last_page,
            current_page=page,
            per_page=c
        )

    async def show_client(self, id: int, db: Session = Depends(get_db)) -> ClientShow:
        return client_repository.get_or_404(db, id)

    async def create_client(self, client: ClientCreate, db: Session = Depends(get_db)) -> ClientShow:
        return client_repository.create(db, obj_in=client)

    async def update_client(self, id: int, client: ClientUpdate, db: Session = Depends(get_db)) -> ClientShow:
        db_client = client_repository.get_or_404(db, id)
        return client_repository.update(db, db_obj=db_client, obj_in=client)

    async def delete_client(self, id: int, db: Session = Depends(get_db)) -> ClientShow:
        db_client = client_repository.get_or_404(db, id)
        return client_repository.remove(db, id=db_client.id)


router = ClientRouter().router
