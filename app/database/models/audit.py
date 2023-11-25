from typing import List

from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, ARRAY
from sqlalchemy.orm import relationship, Mapped

from .base import Base


class Audit(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    url: Mapped[str] = Column(String(150), nullable=False)
    method: Mapped[str] = Column(String(10), nullable=False)
    status: Mapped[int] = Column(Integer, nullable=False)
    session_id: Mapped[int] = Column(Integer, ForeignKey('session.id'), nullable=False)
    session: Mapped["Session"] = relationship('Session', back_populates='audits', lazy='subquery')
