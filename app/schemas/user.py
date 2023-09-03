from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from datetime import datetime

from app.utils.hash_utils import Password


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    email: EmailStr
    realm_id: int


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

    @field_validator('password')
    def encrypt_password(cls, v):
        return Password.encrypt(v)


class UserUpdate(UserBase):
    pass


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(min_length=8, max_length=100)
    new_password: str = Field(min_length=8, max_length=100)

    @field_validator('new_password')
    def encrypt_password(cls, v):
        return Password.encrypt(v)


class UserShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

