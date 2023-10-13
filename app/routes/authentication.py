from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.authentication import AuthenticationLogin
from app.repository.user import user_repository
from app.repository.session import session_repository
from app.schemas.session import SessionCreate
from app.core.dependencies import get_db, CurrentUser
from app.utils.authentication.jwt import JWT


class AuthenticationRouter:
    def __init__(self):
        self.current_user = CurrentUser()
        self.router = APIRouter(tags=['Authentication'])
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/login_test", self.login_test, methods=["POST"])

    def login(self, user: AuthenticationLogin, db: Session = Depends(get_db)):
        db_user = user_repository.find_by_authentication_login(db, user)
        token = JWT().get_token({'user_id': db_user.id})

        session_repository.inactivate_all_active_sessions_by_user_id(db, db_user.id)
        session = SessionCreate(token=token['access'], user_id=db_user.id)
        session_repository.create(db, session)

        return token

    def logout(self, db: Session = Depends(get_db)):
        user_id = JWT().jwt_token_validator(self.current_user.token).get('user_id')
        session_repository.inactivate_all_active_sessions_by_user_id(db, user_id)


router = AuthenticationRouter().router
