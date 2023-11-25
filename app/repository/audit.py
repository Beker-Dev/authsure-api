from .base import RepositoryBase
from app.database.models.audit import Audit
from app.schemas.audit import AuditCreate, AuditUpdate


class AuditRepository(RepositoryBase[Audit, AuditCreate, AuditUpdate]):
    pass


audit_repository = AuditRepository(Audit)
