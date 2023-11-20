from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional, Union


class GroupBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    realm_id: int
    users: Optional[List[int]] = []
    roles: Optional[List[int]] = []


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupShow(GroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class GroupShowPaginated(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_page: int
    last_page: int
    per_page: int
    groups: List[GroupShow]
