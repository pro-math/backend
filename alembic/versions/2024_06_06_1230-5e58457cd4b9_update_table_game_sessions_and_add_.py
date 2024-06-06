"""update table game sessions and add table rating

Revision ID: 5e58457cd4b9
Revises: abf230c77a60
Create Date: 2024-06-06 12:30:59.018320

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String

from src.schemas.enums import EnumArray

# revision identifiers, used by Alembic.
revision: str = "5e58457cd4b9"
down_revision: Union[str, None] = "abf230c77a60"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ratings",
        sa.Column("game_mode", sa.String(), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("math_operations", EnumArray(String()), nullable=False),
        sa.Column("examples_category", sa.Integer(), nullable=False),
        sa.Column("game_session_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_session_id"],
            ["game_sessions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ratings")
    # ### end Alembic commands ###