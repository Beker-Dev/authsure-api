from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship, Mapped

from .base import Base


class Client(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(50), nullable=False, unique=True)
    description: Mapped[str] = Column(Text, nullable=True)
    key: Mapped[str] = Column(String(50), nullable=False, unique=True)
    secret: Mapped[str] = Column(String(255), nullable=False)
    realm_id: Mapped[int] = Column(Integer, ForeignKey('realm.id'), nullable=False)

    realm: Mapped["Realm"] = relationship("Realm", back_populates="clients", lazy="subquery")  # noqa: F821
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="client")  # noqa: F821
    roles: Mapped[List["Role"]] = relationship("Role", secondary="client_role", back_populates="clients")  # noqa: F821
