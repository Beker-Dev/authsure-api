from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from jose.exceptions import JWTError

from app.schemas.authentication import AuthenticationLogin, AuthenticationClientLogin, Token
from app.repository.user import user_repository
from app.repository.client import client_repository
from app.repository.session import session_repository
from app.schemas.session import SessionCreate
from app.schemas.user import CurrentUser
from app.core.dependencies import get_db
from app.utils.authentication.jwt import JWT
from app.core.dependencies import auth_security


class AuthenticationRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Authentication'], prefix='/auth')
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/refresh", self.refresh, methods=["POST"])
        self.router.add_api_route("/check", self.check_token, methods=["POST"])

    # async def login(self, user: AuthenticationLogin, db: Session = Depends(get_db)) -> Token:
    #     db_user = user_repository.find_by_authentication_login(db, user)
    #     token = JWT().get_token({'user_id': db_user.id})
    #
    #     session_repository.inactivate_all_active_sessions_by_user_id(db, db_user.id)
    #     session = SessionCreate(token=token.access, user_id=db_user.id)
    #     session_repository.create(db, session)
    #
    #     return token

    async def logout(self, db: Session = Depends(get_db), current_user: CurrentUser = Depends(auth_security)) -> None:
        user_id = JWT().jwt_token_validator(current_user.token).get('user_id')
        session_repository.inactivate_all_active_sessions_by_user_id(db, user_id)

    async def refresh(self, refresh_token: Token, current_user: CurrentUser = Depends(auth_security)) -> Token:
        try:
            token = JWT().refresh_token(refresh_token.refresh)
            current_user.token = token.access
            return token
        except JWTError as e:
            raise HTTPException(status_code=403, detail=str(e))

    async def login(self, client: AuthenticationClientLogin, db: Session = Depends(get_db)) -> Token:
        # TODO: check if user has permission to access client
        # TODO: ADD DEFAULT INSTANCE FOR EACH ROOT OBJECT

        db_client = client_repository.find_by_authentication_client_login(db, client)
        user = AuthenticationLogin.model_construct(username=client.username, password=client.password)

        db_user = user_repository.find_by_authentication_login(db, user)
        token = JWT().get_token({'user_id': db_user.id, 'client_id': db_client.id})

        session_repository.inactivate_all_active_sessions_by_user_id(db, db_user.id)
        session = SessionCreate(token=token.access, user_id=db_user.id)
        session_repository.create(db, session)

        return token

    async def check_token(self, current_user: CurrentUser = Depends(auth_security)) -> JSONResponse:
        return JSONResponse(JWT().jwt_token_validator(current_user.token))


router = AuthenticationRouter().router
