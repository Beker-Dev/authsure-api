from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base
from app.database.relationship import user_group, group_role


class Group(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    realm_id = Column(Integer, ForeignKey('realm.id'), nullable=False)
    realm = relationship("Realm", back_populates="groups", lazy="subquery")

    users = relationship("User", secondary=user_group, back_populates="groups")
    roles = relationship("Role", secondary=group_role, back_populates="groups")
