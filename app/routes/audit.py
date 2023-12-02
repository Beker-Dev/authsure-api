from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repository.audit import audit_repository
from app.schemas.audit import AuditShow, AuditShowPaginated
from app.core.dependencies import auth_security, permissions_security
from app.core.config import settings
from app.utils.filters.query_filters import DefaultFilter
from app.utils.repository_utils.filters import FilterJoin
from app.database.models.audit import Audit
from app.database.models.realm import Realm
from app.database.models.user import User
from app.database.enums.role_type import RoleType
from app.database.models.session import Session as SessionModel


class AuditRouter:
    def __init__(self):
        self.router = APIRouter(tags=['audits'], prefix='/audits', dependencies=[Depends(auth_security)])
        self.router.add_api_route(
            "",
            self.show_audits,
            response_model=AuditShowPaginated,
            methods=["GET"],
            dependencies=[Depends(permissions_security(RoleType.audit_view))]
        )
        self.router.add_api_route(
            "/{id}",
            self.show_audit,
            response_model=AuditShow,
            methods=["GET"],
            dependencies=[Depends(permissions_security(RoleType.audit_view))]
        )

    async def show_audits(
            self,
            query: DefaultFilter = Depends(DefaultFilter),
            db: Session = Depends(get_db),
            page: int = 1,
            c: int = settings.DEFAULT_PAGE_SIZE
    ) -> AuditShowPaginated:
        filters = [
            FilterJoin(SessionModel, SessionModel.id, Audit.session_id),
            FilterJoin(User, User.id, SessionModel.user_id),
            FilterJoin(Realm, Realm.id, User.realm_id, [query.realm], 'name')
        ]
        result_query = audit_repository.get_by_join(db, filters_join=filters, skip=(page - 1) * c, limit=c)
        last_page_query = audit_repository.get_by_join(db, filters_join=filters)
        audits = result_query.all()
        last_page = audit_repository.get_last_page(last_page_query, c)
        return AuditShowPaginated(
            audits=[AuditShow.model_validate(audit) for audit in audits],
            last_page=last_page,
            current_page=page,
            per_page=c
        )

    async def show_audit(self, id: int, db: Session = Depends(get_db)) -> AuditShow:
        return audit_repository.get_or_404(db, id)


router = AuditRouter().router
