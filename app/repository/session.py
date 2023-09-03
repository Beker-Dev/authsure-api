from sqlalchemy.orm import Session

from .base import RepositoryBase
from app.database.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate


class SessionRepository(RepositoryBase[Session, SessionCreate, SessionUpdate]):
    def inactivate_all_active_sessions_by_user_id(self, db: Session, user_id: int):
        active_sessions = super().get_by(db, {'user_id': user_id, 'is_active': True}, all=True)
        for session in active_sessions:
            session.is_active = False
            db.add(session)
            db.commit()
            db.refresh(session)


session_repository = SessionRepository(Session)