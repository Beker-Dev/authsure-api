from pydantic import BaseModel, model_validator


class AuthenticationBase(BaseModel):
    username: str
    password: str


class AuthenticationLogin(AuthenticationBase):
    pass
