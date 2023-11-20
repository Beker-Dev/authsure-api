from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, Mapped

from .base import Base


class Realm(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(100), nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="realm", cascade="all, delete-orphan")
    clients: Mapped[List["Client"]] = relationship("Client", back_populates="realm", cascade="all, delete-orphan")
    groups: Mapped[List["Group"]] = relationship("Group", back_populates="realm", cascade="all, delete-orphan")
    roles: Mapped[List["Role"]] = relationship("Role", back_populates="realm", cascade="all, delete-orphan")
