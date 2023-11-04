from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class RoleBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleShow(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class RoleShowPaginated(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_page: int
    last_page: int
    per_page: int
    roles: List[RoleShow]
