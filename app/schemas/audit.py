from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class AuditBase(BaseModel):
    url: str = Field(min_length=1, max_length=150)
    method: str = Field(min_length=1, max_length=10)
    headers: list[str]
    status: int
    client_id: int
    user_id: int


class AuditCreate(AuditBase):
    pass


class AuditUpdate(AuditBase):
    pass


class AuditShow(AuditBase):
    # model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

