from pydantic import BaseModel, model_validator
from typing import Optional

from app.utils.schema_utils.formdata_to_json import parse_form_data_to_json
from app.core.config import settings


class AuthenticationBase(BaseModel):
    username: str
    password: str


class AuthenticationLogin(AuthenticationBase):
    pass


class AuthenticationClientLogin(AuthenticationLogin):
    key: str
    secret: str

    @model_validator(mode='before')
    def validate_fields(self):
        if isinstance(self, bytes):
            v = parse_form_data_to_json(self, ['grant_type'])
            v['key'] = settings.DEFAULT_CLIENT_KEY
            v['secret'] = settings.DEFAULT_CLIENT_SECRET
            return v
        return self


class Token(BaseModel):
    access: Optional[str] = ""
    refresh: Optional[str] = ""
    token_type: Optional[str] = ""
