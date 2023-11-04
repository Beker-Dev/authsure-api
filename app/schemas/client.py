from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class ClientBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=255)
    key: str = Field(min_length=1, max_length=50)
    secret: str = Field(min_length=1, max_length=255)
    realm_id: int


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientShow(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class ClientShowPaginated(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_page: int
    last_page: int
    per_page: int
    clients: List[ClientShow]
