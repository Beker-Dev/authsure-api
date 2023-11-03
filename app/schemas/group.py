from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class GroupBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupShow(GroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

