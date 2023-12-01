from fastapi import Request
from typing import Callable, Any

from app.repository.audit import audit_repository
from app.schemas.audit import AuditCreate
from app.core.dependencies import get_db
from app.repository.session import session_repository


class Audit:
    async def __call__(self, request: Request, call_next: Callable) -> Any:
        response = await call_next(request)
        try:
            token = request.headers.get("Authorization").split('Bearer ')[1]
            db = next(get_db())
            db_session = session_repository.get_by(db, {'token': token, 'is_active': True})
            audit_repository.create(
                db=db,
                obj_in=AuditCreate(
                    url=str(request.url),
                    method=request.method,
                    status=response.status_code,
                    session_id=db_session.id
                )
            )
            db.close()
        except Exception as e:
            print(type(e), e)
        return response
