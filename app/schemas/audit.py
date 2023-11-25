from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class AuditBase(BaseModel):
    url: str = Field(min_length=1, max_length=150)
    method: str = Field(min_length=1, max_length=10)
    status: int
    session_id: int


class AuditCreate(AuditBase):
    pass


class AuditUpdate(AuditBase):
    pass


class AuditShow(AuditBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class AuditShowPaginated(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_page: int
    last_page: int
    per_page: int
    audits: list[AuditShow]
