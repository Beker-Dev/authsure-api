from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class RealmBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class RealmCreate(RealmBase):
    pass


class RealmUpdate(RealmBase):
    pass


class RealmShow(RealmBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime
    updated_at: datetime

