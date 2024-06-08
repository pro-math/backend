"""update table achievements

Revision ID: adb866ab5d7c
Revises: f1e69e2ffb98
Create Date: 2024-06-08 11:03:39.028283

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "adb866ab5d7c"
down_revision: Union[str, None] = "f1e69e2ffb98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_achievements",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("achievement_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["achievement_id"],
            ["achievements.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
    )
    op.drop_constraint("users_achievements_ids_fkey", "users", type_="foreignkey")
    op.drop_column("users", "achievements_ids")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("achievements_ids", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "users_achievements_ids_fkey",
        "users",
        "achievements",
        ["achievements_ids"],
        ["id"],
    )
    op.drop_table("user_achievements")
    # ### end Alembic commands ###
