from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    realm_id = Column(Integer, ForeignKey('realm.id'), nullable=False)
