from sqlalchemy import Table, Column, Integer, ForeignKey

from app.database.models.base import Base


group_role = Table(
    "group_role",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("group.id")),
    Column("role_id", Integer, ForeignKey("role.id")),
)
