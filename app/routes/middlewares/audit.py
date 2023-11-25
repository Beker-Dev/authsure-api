from fastapi import Request, Depends
from typing import Callable, Any

from app.repository.audit import audit_repository
from app.schemas.audit import AuditCreate
from app.core.dependencies import get_db
from app.utils.authentication.jwt import JWT


class Audit:
    async def __call__(self, request: Request, call_next: Callable) -> Any:
        response = await call_next(request)
        try:
            token = request.headers.get("Authorization").split('Bearer ')[1]
            token_info = JWT().jwt_token_validator(token)
            audit_repository.create(
                db=next(get_db()),
                obj_in=AuditCreate(
                    url=str(request.url),
                    method=request.method,
                    headers=[str({header[0]: header[1]}) for header in request.headers.items()],
                    status=response.status_code,
                    client_id=token_info.get('client_id'),
                    user_id=token_info.get('user_id')
                )
            )
        except Exception as e:
            print(type(e), e)
        return response
