from pydantic import BaseModel

from typing import Optional


class DefaultFilter(BaseModel):
    realm: str
