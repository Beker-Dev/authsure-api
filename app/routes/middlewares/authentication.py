from fastapi import Request, Response
from typing import Callable

from app.utils.authentication.jwt import JWT


class Authentication:
    def __init__(self):
        self.jwt = JWT()

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        try:
            token = request.headers.get('authorization').split('Bearer ')[1]
            self.jwt.jwt_token_validator(token)
        except:
            return Response(content='Invalid Token', status_code=401)
        else:
            return await call_next(request)
