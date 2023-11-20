from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from datetime import datetime
from typing import List, Optional, Any

from app.utils.hash_utils import Password
from .association import UserRoleShow, UserGroupShow


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    email: EmailStr
    realm_id: int
    groups: Optional[List[Any]] = []
    roles: Optional[List[Any]] = []


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

    @field_validator('password')
    def encrypt_password(cls, v):
        return Password.encrypt(v)


class UserUpdate(UserBase):
    pass


class UserShow(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    groups: Optional[List[UserGroupShow]] = []
    roles: Optional[List[UserRoleShow]] = []
    created_at: datetime
    updated_at: datetime


class UserShowPaginated(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_page: int
    last_page: int
    per_page: int
    users: List[UserShow]


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(min_length=8, max_length=100)
    new_password: str = Field(min_length=8, max_length=100)

    @field_validator('new_password')
    def encrypt_password(cls, v):
        return Password.encrypt(v)


class CurrentUser(BaseModel):
    user: UserShow
    token: str


class UserRecoverPassword(BaseModel):
    email: EmailStr
