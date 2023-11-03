from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class SessionBase(BaseModel):
    token: str = Field(min_length=1, max_length=255)
    is_active: bool = Field(default=True)
    user_id: int


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SessionBase):
    pass


class SessionShow(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

