from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from app.repository.user import user_repository
from app.schemas.user import UserShow, UserCreate, UserUpdate, UserPasswordUpdate, UserShowPaginated, UserRecoverPassword
from app.utils.hash_utils.password import Password
from app.utils.database_utils import PopulateDatabase
from app.core.dependencies import auth_security, permissions_security
from app.core.config import settings
from app.utils.filters.query_filters import DefaultFilter
from app.utils.repository_utils.filters import FilterJoin
from app.database.models.user import User
from app.database.models.realm import Realm
from app.utils.password.password_generator import password_generator
from app.service.smtp.sender import send_email
from app.utils.hash_utils.password import Password
from app.database.enums.role_type import RoleType


class UserRouter:
    def __init__(self):
        self.router = APIRouter(tags=['Users'], prefix='/users', dependencies=[Depends(auth_security)])
        self.unsecure_router = APIRouter(tags=['Users'], prefix='/users')
        self.router.add_api_route(
            "",
            self.show_users,
            response_model=UserShowPaginated,
            methods=["GET"],
            dependencies=[Depends(permissions_security(RoleType.user_view))]
        )
        self.router.add_api_route(
            "/{id}",
            self.show_user,
            response_model=UserShow,
            methods=["GET"],
            dependencies=[Depends(permissions_security(RoleType.user_view))]
        )
        self.router.add_api_route(
            "",
            self.create_user,
            response_model=UserShow,
            methods=["POST"],
            dependencies=[Depends(permissions_security(RoleType.user_create))]
        )
        self.router.add_api_route(
            "/{id}",
            self.update_user,
            response_model=UserShow,
            methods=["PUT"],
            dependencies=[Depends(permissions_security(RoleType.user_update))]
        )
        self.router.add_api_route(
            "/{id}",
            self.update_user_password,
            response_model=UserShow,
            methods=["PATCH"]
        )
        self.router.add_api_route(
            "/{id}",
            self.delete_user,
            response_model=UserShow,
            methods=["DELETE"],
            dependencies=[Depends(permissions_security(RoleType.user_delete))]
        )
        self.unsecure_router.add_api_route(
            "/recover-password",
            self.recover_password,
            methods=["POST"]
        )

    async def show_users(
            self,
            query: DefaultFilter = Depends(DefaultFilter),
            db: Session = Depends(get_db),
            page: int = 1,
            c: int = settings.DEFAULT_PAGE_SIZE
    ) -> UserShowPaginated:
        filters = [FilterJoin(Realm, Realm.id, User.realm_id, [query.realm], 'name')]
        result_query = user_repository.get_by_join(db, filters_join=filters, skip=(page - 1) * c, limit=c)
        last_page_query = user_repository.get_by_join(db, filters_join=filters)
        users = result_query.all()
        last_page = user_repository.get_last_page(last_page_query, c)
        return UserShowPaginated(
            users=[UserShow.model_validate(user) for user in users],
            last_page=last_page,
            current_page=page,
            per_page=c
        )

    async def show_user(self, id: int, db: Session = Depends(get_db)) -> UserShow:
        return user_repository.get_or_404(db, id)

    async def create_user(self, user: UserCreate, db: Session = Depends(get_db)) -> UserShow:
        return user_repository.create(db, obj_in=user)

    async def update_user(self, id: int, user: UserUpdate, db: Session = Depends(get_db)) -> UserShow:
        db_user = user_repository.get_or_404(db, id)
        return user_repository.update(db, db_obj=db_user, obj_in=user)

    async def update_user_password(
            self,
            id: int, user_password: UserPasswordUpdate,
            db: Session = Depends(get_db)
    ) -> UserShow:
        db_user = user_repository.get_or_404(db, id)
        if Password.check(user_password.old_password, db_user.password):
            return user_repository.update_password(db, db_user, user_password.new_password)
        raise HTTPException(400, "Invalid password")

    async def delete_user(self, id: int, db: Session = Depends(get_db)) -> UserShow:
        db_user = user_repository.get_or_404(db, id)
        return user_repository.remove(db, id=db_user.id)

    async def recover_password(self, user: UserRecoverPassword, db: Session = Depends(get_db)) -> Response:
        db_user = user_repository.get_by(db=db, filters={'email': user.email})
        if not db_user:
            raise HTTPException(422, "Email not found")
        else:
            new_password = password_generator()
            user_repository.update_password(db, db_user, Password.encrypt(new_password))
            send_email(f"\nYour new password is: {new_password}\n\n\nPlease, change it ASAP!", db_user)
            return Response(f"Temporary password has been sent to {user.email}")


router = UserRouter().unsecure_router
router.include_router(UserRouter().router)
