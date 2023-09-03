from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base
from app.database.relationship import user_role, group_role


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    users = relationship("User", secondary=user_role, back_populates="roles")
    groups = relationship("Group", secondary=group_role, back_populates="roles")
