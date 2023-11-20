from pydantic import BaseModel, ConfigDict
from datetime import datetime


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
    created_at: datetime
    updated_at: datetime


class GroupRoleShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    realm_id: int
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
