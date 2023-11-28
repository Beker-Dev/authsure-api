from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from jose.exceptions import JWTError

from app.schemas.authentication import AuthenticationLogin, AuthenticationClientLogin, Token
from app.repository.user import user_repository
from app.repository.client import client_repository
from app.repository.session import session_repository
from app.schemas.session import SessionCreate, SessionUpdate
from app.schemas.user import CurrentUser
from app.core.dependencies import get_db
from app.utils.authentication.jwt import JWT
from app.core.dependencies import auth_security
from app.utils.authentication.permissions import check_permissions

from app.repository.user import user_repository
from app.schemas.user import UserRecoverPassword
from app.utils.password.password_generator import password_generator
from app.service.smtp.sender import send_email
from fastapi import Response
from app.utils.hash_utils.password import Password


class AuthenticationRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Authentication'], prefix='/auth')
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/refresh", self.refresh, methods=["POST"])
        self.router.add_api_route("/check", self.check_token, methods=["POST"])
        self.router.add_api_route(
            "/recover-password",
            self.recover_password,
            methods=["POST"]
        )

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

    async def refresh(self, refresh_token: Token, db: Session = Depends(get_db)) -> Token:
        try:
            refreshed_token = JWT().refresh_token(refresh_token.refresh)
            db_session = session_repository.get_by(db, {'token': refresh_token.access, 'is_active': True})
            session_repository.inactivate_all_active_sessions_by_user_id(db, db_session.user_id)
            session_repository.update(
                db,
                db_session,
                SessionUpdate(
                    token=refreshed_token.access,
                    user_id=db_session.user_id,
                    client_id=db_session.client_id,
                    is_active=True
                )
            )
            return refreshed_token
        except JWTError as e:
            raise HTTPException(status_code=403, detail=str(e))
        except AttributeError as e:
            raise HTTPException(status_code=403, detail="Invalid token information in records")

    async def login(self, client: AuthenticationClientLogin, db: Session = Depends(get_db)) -> Token:
        db_client = client_repository.find_by_authentication_client_login(db, client)
        user = AuthenticationLogin.model_construct(username=client.username, password=client.password)

        db_user = user_repository.find_by_authentication_login(db, user)

        check_permissions(db_user, db_client)

        token = JWT().get_token({'user_id': db_user.id, 'client_id': db_client.id})

        session_repository.inactivate_all_active_sessions_by_user_id(db, db_user.id)
        session = SessionCreate(token=token.access, user_id=db_user.id, client_id=db_client.id)
        session_repository.create(db, session)

        return token

    async def check_token(self, current_user: CurrentUser = Depends(auth_security)) -> JSONResponse:
        return JSONResponse(JWT().jwt_token_validator(current_user.token))

    async def recover_password(self, user: UserRecoverPassword, db: Session = Depends(get_db)) -> Response:
        db_user = user_repository.get_by(db=db, filters={'email': user.email})
        if not db_user:
            raise HTTPException(422, "Email not found")
        else:
            new_password = password_generator()
            user_repository.update_password(db, db_user, Password.encrypt(new_password))
            send_email(f"\nYour new password is: {new_password}\n\n\nPlease, change it ASAP!", db_user)
            return Response(f"Temporary password has been sent to {user.email}")


router = AuthenticationRouter().router
