from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from app.database.enums.role_type import RoleType


class UserGroupShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    realm_id: int
    created_at: datetime
    updated_at: datetime


class UserRoleShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    realm_id: int
    types: List[RoleType]
    created_at: datetime
    updated_at: datetime


class GroupRoleShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    realm_id: int
    types: List[RoleType]
    created_at: datetime
    updated_at: datetime


class GroupUserShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    realm_id: int
    created_at: datetime
    updated_at: datetime


class ClientRoleShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    realm_id: int
    types: List[RoleType]
    created_at: datetime
    updated_at: datetime


class RoleClientShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    key: str
    secret: str
    realm_id: int
    created_at: datetime
    updated_at: datetime
