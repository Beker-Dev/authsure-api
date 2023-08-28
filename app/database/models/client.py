from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class Client(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    key = Column(String(50), nullable=False)
    secret_char = Column(String(255), nullable=False)
    realm_id = Column(Integer, ForeignKey('realm.id'))