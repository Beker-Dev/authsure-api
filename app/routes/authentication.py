from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.schemas.authentication import AuthenticationLogin
from app.repository.user import user_repository
from app.repository.session import session_repository
from app.schemas.session import SessionCreate
from app.core.dependencies import get_db
from app.utils.authentication.jwt import JWT


router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user: AuthenticationLogin, db: Session = Depends(get_db)):
    db_user = user_repository.find_by_authentication_login(db, user)
    token = JWT().get_token({'user_id': db_user.id})

    session_repository.inactivate_all_active_sessions_by_user_id(db, db_user.id)
    session = SessionCreate(token=token['access'], user_id=db_user.id)
    session_repository.create(db, session)

    return token


@router.post('/logout')
def logout(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get('authorization').split('Bearer ')[1]
    user_id = JWT().jwt_token_validator(token).get('user_id')
    session_repository.inactivate_all_active_sessions_by_user_id(db, user_id)
