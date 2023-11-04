from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class RealmBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class RealmCreate(RealmBase):
    pass


class RealmUpdate(RealmBase):
    pass


class RealmShow(RealmBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class RealmShowPaginated(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_page: int
    last_page: int
    per_page: int
    realms: List[RealmShow]
