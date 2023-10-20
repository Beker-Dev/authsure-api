from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from jose.exceptions import JWTError

from app.schemas.authentication import AuthenticationLogin, Token
from app.repository.user import user_repository
from app.repository.session import session_repository
from app.schemas.session import SessionCreate
from app.core.dependencies import get_db, CurrentUser
from app.utils.authentication.jwt import JWT


class AuthenticationRouter:
    def __init__(self):
        self.current_user = CurrentUser()
        self.router = APIRouter(tags=['Authentication'], prefix='/auth')
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/refresh", self.refresh, methods=["POST"])

    async def login(self, user: AuthenticationLogin, db: Session = Depends(get_db)) -> Token:
        db_user = user_repository.find_by_authentication_login(db, user)
        token = JWT().get_token({'user_id': db_user.id})

        session_repository.inactivate_all_active_sessions_by_user_id(db, db_user.id)
        session = SessionCreate(token=token.access, user_id=db_user.id)
        session_repository.create(db, session)

        return token

    async def logout(self, db: Session = Depends(get_db)) -> None:
        user_id = JWT().jwt_token_validator(self.current_user.token).get('user_id')
        session_repository.inactivate_all_active_sessions_by_user_id(db, user_id)

    async def refresh(self, refresh_token: Token) -> Token:
        try:
            token = JWT().refresh_token(refresh_token.refresh)
            self.current_user.token = token.access
            return token
        except JWTError as e:
            raise HTTPException(status_code=403, detail=str(e))


router = AuthenticationRouter().router
