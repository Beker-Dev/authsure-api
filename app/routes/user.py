from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.user import user_repository
from app.schemas.user import UserShow, UserCreate, UserUpdate, UserPasswordUpdate
from app.utils.hash_utils.password import Password
from app.utils.database_utils import PopulateDatabase


class UserRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Users'], prefix='/users')
        self.router.add_api_route("", self.show_users, response_model=List[UserShow], methods=["GET"])
        self.router.add_api_route("/{id}", self.show_user, response_model=UserShow, methods=["GET"])
        self.router.add_api_route("", self.create_user, response_model=UserShow, methods=["POST"])
        self.router.add_api_route("/{id}", self.update_user, response_model=UserShow, methods=["PUT"])
        self.router.add_api_route("/{id}", self.update_user_password, response_model=UserShow, methods=["PATCH"])
        self.router.add_api_route("/{id}", self.delete_user, response_model=UserShow, methods=["DELETE"])
        self.router.add_api_route("/recover-password", self.recover_password, methods=["POST"])

    async def show_users(self, db: Session = Depends(get_db)):
        return user_repository.get_multi(db)

    async def show_user(self, id: int, db: Session = Depends(get_db)):
        return user_repository.get_or_404(db, id)

    async def create_user(self, user: UserCreate, db: Session = Depends(get_db)):
        return user_repository.create(db, obj_in=user)

    async def update_user(self, id: int, user: UserUpdate, db: Session = Depends(get_db)):
        db_user = user_repository.get_or_404(db, id)
        return user_repository.update(db, db_obj=db_user, obj_in=user)

    async def update_user_password(self, id: int, user_password: UserPasswordUpdate, db: Session = Depends(get_db)):
        db_user = user_repository.get_or_404(db, id)
        if Password.check(user_password.old_password, db_user.password):
            return user_repository.update_password(db, db_user, user_password.new_password)
        raise HTTPException(400, "Invalid password")

    async def delete_user(self, id: int, db: Session = Depends(get_db)):
        db_user = user_repository.get_or_404(db, id)
        return user_repository.remove(db, id=db_user.id)

    async def recover_password(self, db: Session = Depends(get_db)):
        raise NotImplementedError


router = UserRouter().router
