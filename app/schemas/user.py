from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=100)
    email: EmailStr
    realm_id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

