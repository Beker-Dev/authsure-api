from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import as_declarative, declared_attr, declared_attr
from app.utils.generic import camel_to_snake


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
