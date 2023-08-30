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


@router.get("/{id}", response_model=SessionShow)
async def show_session(id: int, db: Session = Depends(get_db)):
    return session_repository.get_or_404(db, id)


@router.post("", response_model=SessionShow)
async def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    return session_repository.create(db, obj_in=session)


@router.put("/{id}", response_model=SessionShow)
async def update_session(id: int, session: SessionUpdate, db: Session = Depends(get_db)):
    db_session = session_repository.get_or_404(db, id)
    return session_repository.update(db, db_obj=db_session, obj_in=session)


@router.delete("/{id}", response_model=SessionShow)
async def delete_session(id: int, db: Session = Depends(get_db)):
    db_session = session_repository.get_or_404(db, id)
    return session_repository.remove(db, id=db_session.id)
