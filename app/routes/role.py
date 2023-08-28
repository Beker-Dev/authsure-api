from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.role import role_repository
from app.schemas.role import RoleShow, RoleCreate, RoleUpdate


router = APIRouter(tags=['Roles'], prefix='/roles')


@router.get("", response_model=List[RoleShow])
async def show_roles(db: Session = Depends(get_db)):
    return role_repository.get_multi(db)


@router.get("/{id}", response_model=RoleShow)
async def show_role(id: int, db: Session = Depends(get_db)):
    return role_repository.get_or_404(db, id)


@router.post("", response_model=RoleShow)
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_repository.create(db, obj_in=role)


@router.put("/{id}", response_model=RoleShow)
async def update_role(id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = role_repository.get_or_404(db, id)
    return role_repository.update(db, db_obj=db_role, obj_in=role)


@router.delete("/{id}", response_model=RoleShow)
async def delete_role(id: int, db: Session = Depends(get_db)):
    db_role = role_repository.get_or_404(db, id)
    return role_repository.remove(db, id=db_role.id)
