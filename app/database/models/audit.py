from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, ARRAY
from sqlalchemy.orm import relationship, Mapped

from .base import Base


class Audit(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    url: Mapped[str] = Column(String(150), nullable=False)
    method: Mapped[str] = Column(String(10), nullable=False)
    headers: Mapped[List[str]] = Column(ARRAY(String), nullable=True)
    status: Mapped[int] = Column(Integer, nullable=False)
    client_id: Mapped[int] = Column(Integer, ForeignKey('client.id'), nullable=False)
    user_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=True)
    client: Mapped["Client"] = relationship("Client", back_populates="audits", lazy="subquery")
    user: Mapped["User"] = relationship("User", back_populates="audits", lazy="subquery")
