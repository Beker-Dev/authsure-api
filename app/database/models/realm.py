from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from .base import Base


class Realm(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(100), nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="realm", cascade="all, delete-orphan")  # noqa: F821, E501
    clients: Mapped[List["Client"]] = relationship("Client", back_populates="realm", cascade="all, delete-orphan")  # noqa: F821, E501
    groups: Mapped[List["Group"]] = relationship("Group", back_populates="realm", cascade="all, delete-orphan")  # noqa: F821, E501
    roles: Mapped[List["Role"]] = relationship("Role", back_populates="realm", cascade="all, delete-orphan")  # noqa: F821, E501
