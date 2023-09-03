from sqlalchemy import Table, Column, Integer, ForeignKey

from app.database.models.base import Base


user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("group_id", Integer, ForeignKey("group.id")),
)
