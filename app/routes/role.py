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
