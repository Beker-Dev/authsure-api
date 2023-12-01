from pydantic import BaseModel


class DefaultFilter(BaseModel):
    realm: str
