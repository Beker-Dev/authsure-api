from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped

from .base import Base
from app.database.relationship import user_group, user_role


class User(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(String(100), nullable=False, unique=True)
    password: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True)
    realm_id: Mapped[int] = Column(Integer, ForeignKey('realm.id'), nullable=False)
    realm: Mapped["Realm"] = relationship("Realm", back_populates="users", lazy="subquery")  # noqa: F821

    groups: Mapped[List["Group"]] = relationship("Group", secondary=user_group, back_populates="users")  # noqa: F821
    roles: Mapped[List["Role"]] = relationship("Role", secondary=user_role, back_populates="users")  # noqa: F821
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="user")  # noqa: F821
