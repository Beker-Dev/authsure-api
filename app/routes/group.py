from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.group import group_repository
from app.schemas.group import GroupShow, GroupCreate, GroupUpdate, GroupShowPaginated
from app.core.dependencies import auth_security
from app.core.config import settings


class GroupRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Groups'], prefix='/groups', dependencies=[Depends(auth_security)])
        self.router.add_api_route("", self.show_groups, response_model=GroupShowPaginated, methods=["GET"])
        self.router.add_api_route("/{id}", self.show_group, response_model=GroupShow, methods=["GET"])
        self.router.add_api_route("", self.create_group, response_model=GroupShow, methods=["POST"])
        self.router.add_api_route("/{id}", self.update_group, response_model=GroupShow, methods=["PUT"])
        self.router.add_api_route("/{id}", self.delete_group, response_model=GroupShow, methods=["DELETE"])

    async def show_groups(
            self,
            db: Session = Depends(get_db),
            page: int = 1,
            c: int = settings.DEFAULT_PAGE_SIZE
    ) -> GroupShowPaginated:
        groups = group_repository.get_multi(db, skip=(page - 1) * c, limit=c)
        last_page = group_repository.get_last_page(db, c)
        return GroupShowPaginated(
            groups=[GroupShow.model_validate(group) for group in groups],
            last_page=last_page,
            current_page=page,
            per_page=c
        )

    async def show_group(self, id: int, db: Session = Depends(get_db)) -> GroupShow:
        return group_repository.get_or_404(db, id)

    async def create_group(self, group: GroupCreate, db: Session = Depends(get_db)) -> GroupShow:
        return group_repository.create(db, obj_in=group)

    async def update_group(self, id: int, group: GroupUpdate, db: Session = Depends(get_db)) -> GroupShow:
        db_group = group_repository.get_or_404(db, id)
        return group_repository.update(db, db_obj=db_group, obj_in=group)

    async def delete_group(self, id: int, db: Session = Depends(get_db)) -> GroupShow:
        db_group = group_repository.get_or_404(db, id)
        return group_repository.remove(db, id=db_group.id)


router = GroupRouter().router
