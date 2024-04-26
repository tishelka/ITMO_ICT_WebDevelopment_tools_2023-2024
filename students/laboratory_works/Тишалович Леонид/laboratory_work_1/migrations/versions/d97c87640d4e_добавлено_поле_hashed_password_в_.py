"""Добавлено поле hashed_password в participant

Revision ID: d97c87640d4e
Revises: 103ecaa86fff
Create Date: 2024-04-26 22:16:37.692984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd97c87640d4e'
down_revision: Union[str, None] = '103ecaa86fff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('participants', sa.Column('hashed_password', sa.String))


def downgrade():
    op.drop_column('participants', 'hashed_password')

