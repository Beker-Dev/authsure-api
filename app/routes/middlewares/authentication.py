# from fastapi import Request
# from fastapi.responses import JSONResponse
# from typing import Callable
#
# from app.utils.authentication.jwt import JWT
# from app.core.dependencies import CurrentUser
#
#
# class Authentication:
#     def __init__(self):
#         self.current_user = CurrentUser()
#         self.jwt = JWT()
#
#     async def __call__(self, request: Request, call_next: Callable) -> JSONResponse:
#         return await call_next(request)
#
#         bypass_routes = ['/docs', '/openapi.json', '/api/auth/login', '/api/auth/refresh']
#
#         if request.url.path in bypass_routes:
#             return await call_next(request)
#
#         try:
#             token = request.headers.get('Authorization').split('Bearer ')[1]
#             self.jwt.jwt_token_validator(token)
#             self.current_user.token = token
#
#             session = session_repository.get_by(next(get_db()), {'token': token})
#             if not session or not session.is_active:
#                 raise Exception
#         except Exception as e:
#             return JSONResponse(content={'detail': 'Invalid token'}, status_code=401)
#         else:
#             return await call_next(request)
