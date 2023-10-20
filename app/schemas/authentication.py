from pydantic import BaseModel, model_validator
from typing import Optional


class AuthenticationBase(BaseModel):
    username: str
    password: str


class AuthenticationLogin(AuthenticationBase):
    pass


class Token(BaseModel):
    access: Optional[str] = ""
    refresh: Optional[str] = ""
    token_type: Optional[str] = ""
