from sqlalchemy import Table, Column, Integer, ForeignKey

from app.database.models.base import Base


client_role = Table(
    "client_role",
    Base.metadata,
    Column("client_id", Integer, ForeignKey("client.id")),
    Column("role_id", Integer, ForeignKey("role.id")),
)
