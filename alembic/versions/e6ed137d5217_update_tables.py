"""update_tables

Revision ID: e6ed137d5217
Revises: e7a9904fb262
Create Date: 2023-11-20 15:47:48.241658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6ed137d5217'
down_revision: Union[str, None] = 'e7a9904fb262'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('realm_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'group', 'realm', ['realm_id'], ['id'])
    op.add_column('role', sa.Column('realm_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'role', 'realm', ['realm_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'role', type_='foreignkey')
    op.drop_column('role', 'realm_id')
    op.drop_constraint(None, 'group', type_='foreignkey')
    op.drop_column('group', 'realm_id')
    # ### end Alembic commands ###
