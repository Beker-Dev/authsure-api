from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, Mapped

from .base import Base


class Session(Base):
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    token: Mapped[str] = Column(String(255), nullable=False)
    is_active: Mapped[bool] = Column(Boolean, nullable=False, default=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=False)
