from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, ARRAY, Enum
from sqlalchemy.orm import relationship, Mapped

from .base import Base
from app.database.relationship import user_role, group_role, client_role
from app.database.enums.role_type import RoleType


class Role(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(100), nullable=False, unique=True)
    types: Mapped[List[RoleType]] = Column(ARRAY(Enum(RoleType)), nullable=False)
    realm_id: Mapped[int] = Column(Integer, ForeignKey('realm.id'), nullable=False)
    realm: Mapped["Realm"] = relationship("Realm", back_populates="roles", lazy="subquery")

    users: Mapped[List["User"]] = relationship("User", secondary=user_role, back_populates="roles")
    groups: Mapped[List["Group"]] = relationship("Group", secondary=group_role, back_populates="roles")
    clients: Mapped[List["Client"]] = relationship("Client", secondary=client_role, back_populates="roles")
