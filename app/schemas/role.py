from pydantic import BaseModel, Field
from datetime import datetime


class RoleBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleShow(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
