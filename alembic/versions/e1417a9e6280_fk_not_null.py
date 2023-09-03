"""fk not null

Revision ID: e1417a9e6280
Revises: 64e88597734a
Create Date: 2023-09-03 11:27:30.642549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1417a9e6280'
down_revision: Union[str, None] = '64e88597734a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client', 'realm_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('session', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user', 'realm_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'realm_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('session', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('client', 'realm_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
