from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.group import group_repository
from app.schemas.group import GroupShow, GroupCreate, GroupUpdate

router = APIRouter(tags=['Groups'], prefix='/groups')


@router.get("", response_model=List[GroupShow])
async def show_groups(db: Session = Depends(get_db)):
    return group_repository.get_multi(db)


@router.get("/{id}", response_model=GroupShow)
async def show_group(id: int, db: Session = Depends(get_db)):
    return group_repository.get_or_404(db, id)


@router.post("", response_model=GroupShow)
async def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    return group_repository.create(db, obj_in=group)


@router.put("/{id}", response_model=GroupShow)
async def update_group(id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    db_group = group_repository.get_or_404(db, id)
    return group_repository.update(db, db_obj=db_group, obj_in=group)


@router.delete("/{id}", response_model=GroupShow)
async def delete_group(id: int, db: Session = Depends(get_db)):
    db_group = group_repository.get_or_404(db, id)
    return group_repository.remove(db, id=db_group.id)
