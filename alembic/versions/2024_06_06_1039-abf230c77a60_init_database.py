"""init database

Revision ID: abf230c77a60
Revises: 
Create Date: 2024-06-06 10:39:37.562003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abf230c77a60'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('game_sessions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('game_mode', sa.String(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('math_operations', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('examples_category', sa.Integer(), nullable=False),
    sa.Column('examples', sa.JSON(), nullable=False),
    sa.Column('total_count', sa.Integer(), nullable=False),
    sa.Column('correct_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game_sessions')
    op.drop_table('users')
    # ### end Alembic commands ###