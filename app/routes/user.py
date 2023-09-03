from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.user import user_repository
from app.schemas.user import UserShow, UserCreate, UserUpdate, UserPasswordUpdate
from app.utils.hash_utils.password import Password
from app.utils.database_utils import PopulateDatabase


router = APIRouter(tags=['Users'], prefix='/users')


@router.get("", response_model=List[UserShow])
async def show_users(db: Session = Depends(get_db)):
    return user_repository.get_multi(db)


@router.get("/{id}", response_model=UserShow)
async def show_user(id: int, db: Session = Depends(get_db)):
    return user_repository.get_or_404(db, id)


@router.post("", response_model=UserShow)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_repository.create(db, obj_in=user)


@router.put("/{id}", response_model=UserShow)
async def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_repository.get_or_404(db, id)
    return user_repository.update(db, db_obj=db_user, obj_in=user)


@router.patch("/{id}", response_model=UserShow)
async def update_user_password(id: int, user_password: UserPasswordUpdate, db: Session = Depends(get_db)):
    db_user = user_repository.get_or_404(db, id)
    if Password.check(user_password.old_password, db_user.password):
        return user_repository.update_password(db, db_user, user_password.new_password)
    raise HTTPException(400, "Invalid password")


@router.delete("/{id}", response_model=UserShow)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = user_repository.get_or_404(db, id)
    return user_repository.remove(db, id=db_user.id)
