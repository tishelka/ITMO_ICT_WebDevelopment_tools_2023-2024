"""Переименовано поле с hashed_password на password

Revision ID: e040c6b9b66f
Revises: d97c87640d4e
Create Date: 2024-04-26 23:58:25.749828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e040c6b9b66f'
down_revision: Union[str, None] = 'd97c87640d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('participants', 'hashed_password', new_column_name='password')


def downgrade():
    op.alter_column('participants', 'password', new_column_name='hashed_password')

