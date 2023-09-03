from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Text
from sqlalchemy.orm import relationship

from .base import Base


class Client(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    key = Column(String(50), nullable=False)
    secret = Column(String(255), nullable=False)
    realm_id = Column(Integer, ForeignKey('realm.id'), nullable=False)
