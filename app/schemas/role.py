from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class RoleBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

