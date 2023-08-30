from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class Session(Base):
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    #user_id = Column(Integer, ForeignKey('user.id'))
