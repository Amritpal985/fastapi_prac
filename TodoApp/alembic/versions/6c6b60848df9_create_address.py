"""create address

Revision ID: 6c6b60848df9
Revises: 
Create Date: 2025-09-01 23:38:09.464786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c6b60848df9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address', sa.String()))
    

def downgrade() -> None:
    op.drop_column('users', 'address')
