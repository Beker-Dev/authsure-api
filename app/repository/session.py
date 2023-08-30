from .base import RepositoryBase
from app.database.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate


class SessionRepository(RepositoryBase[Session, SessionCreate, SessionUpdate]):
    pass


session_repository = SessionRepository(Session)