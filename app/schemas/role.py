from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Any, Optional

from app.database.enums.role_type import RoleType
from .association import RoleClientShow
from .realm import RealmShow


class RoleBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    realm_id: int
    types: List[RoleType]
    clients: Optional[List[Any]] = []


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleShow(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    realm: RealmShow
    clients: Optional[List[RoleClientShow]] = []
    created_at: datetime
    updated_at: datetime


class RoleShowPaginated(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_page: int
    last_page: int
    per_page: int
    roles: List[RoleShow]
