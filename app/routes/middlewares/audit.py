from fastapi import Request, Depends
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
                    headers=[str({header[0]: header[1]}) for header in request.headers.items()],
                    status=response.status_code,
                    client_id=db_session.client_id,
                    user_id=db_session.user_id
                )
            )
            db.close()
        except Exception as e:
            print(type(e), e)
        return response
