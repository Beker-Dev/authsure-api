from sqlalchemy import Table, Column, Integer, ForeignKey

from app.database.models.base import Base


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("role_id", Integer, ForeignKey("role.id")),
)
