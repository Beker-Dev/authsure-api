from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped

from .base import Base
from app.database.relationship import user_group, group_role


class Group(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(100), nullable=False, unique=True)
    realm_id: Mapped[int] = Column(Integer, ForeignKey('realm.id'), nullable=False)
    realm: Mapped["Realm"] = relationship("Realm", back_populates="groups", lazy="subquery")  # noqa: F821

    users: Mapped[List["User"]] = relationship("User", secondary=user_group, back_populates="groups")  # noqa: F821
    roles: Mapped[List["Role"]] = relationship("Role", secondary=group_role, back_populates="groups")  # noqa: F821
