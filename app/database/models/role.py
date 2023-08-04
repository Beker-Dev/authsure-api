from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
