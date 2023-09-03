from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base
from app.database.relationship import user_group, user_role


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    realm_id = Column(Integer, ForeignKey('realm.id'), nullable=False)
    realm = relationship("Realm", back_populates="users", lazy="subquery")

    groups = relationship("Group", secondary=user_group, back_populates="users")
    roles = relationship("Role", secondary=user_role, back_populates="users")
