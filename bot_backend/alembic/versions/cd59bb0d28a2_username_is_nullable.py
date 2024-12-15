"""username is nullable

Revision ID: cd59bb0d28a2
Revises: ffb011443768
Create Date: 2024-12-09 09:01:30.105603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd59bb0d28a2'
down_revision: Union[str, None] = 'ffb011443768'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'username',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Users', 'username',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    # ### end Alembic commands ###
