from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.session import session_repository
from app.schemas.session import SessionShow, SessionCreate, SessionUpdate


router = APIRouter(tags=['Sessions'], prefix='/sessions')


@router.get("", response_model=List[SessionShow])
async def show_sessions(db: Session = Depends(get_db)):
    return session_repository.get_multi(db)
