from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.session import session_repository
from app.schemas.session import SessionShow, SessionCreate, SessionUpdate, SessionShowPaginated
from app.core.dependencies import auth_security
from app.core.config import settings


class SessionRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Sessions'], prefix='/sessions', dependencies=[Depends(auth_security)])
        self.router.add_api_route('', self.show_sessions, response_model=SessionShowPaginated, methods=['GET'])
        self.router.add_api_route('/{id}', self.show_session, response_model=SessionShow, methods=['GET'])
        self.router.add_api_route('', self.create_session, response_model=SessionShow, methods=['POST'])
        self.router.add_api_route('/{id}', self.update_session, response_model=SessionShow, methods=['PUT'])
        self.router.add_api_route('/{id}', self.delete_session, response_model=SessionShow, methods=['DELETE'])

    async def show_sessions(
            self,
            db: Session = Depends(get_db),
            page: int = 1,
            c: int = settings.DEFAULT_PAGE_SIZE
    ) -> SessionShowPaginated:
        sessions = session_repository.get_multi(db, skip=(page - 1) * c, limit=c)
        last_page = session_repository.get_last_page(db, c)
        return SessionShowPaginated(
            sessions=[SessionShow.model_validate(session) for session in sessions],
            last_page=last_page,
            current_page=page,
            per_page=c
        )

    async def show_session(self, id: int, db: Session = Depends(get_db)) -> SessionShow:
        return session_repository.get_or_404(db, id)

    async def create_session(self, session: SessionCreate, db: Session = Depends(get_db)) -> SessionShow:
        return session_repository.create(db, obj_in=session)

    async def update_session(self, id: int, session: SessionUpdate, db: Session = Depends(get_db)) -> SessionShow:
        db_session = session_repository.get_or_404(db, id)
        return session_repository.update(db, db_obj=db_session, obj_in=session)

    async def delete_session(self, id: int, db: Session = Depends(get_db)) -> SessionShow:
        db_session = session_repository.get_or_404(db, id)
        return session_repository.remove(db, id=db_session.id)


router = SessionRouter().router
