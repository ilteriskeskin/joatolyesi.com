"""Planlı dinlenme günü: practice_logs.is_rest_day, discipline/minutes nullable

Revision ID: 0011
Revises: 0010
"""

import sqlalchemy as sa
from alembic import op

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "practice_logs",
        sa.Column("is_rest_day", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.alter_column("practice_logs", "discipline", existing_type=sa.String(20), nullable=True)
    op.alter_column("practice_logs", "minutes", existing_type=sa.Integer(), nullable=True)


def downgrade() -> None:
    op.alter_column("practice_logs", "minutes", existing_type=sa.Integer(), nullable=False)
    op.alter_column("practice_logs", "discipline", existing_type=sa.String(20), nullable=False)
    op.drop_column("practice_logs", "is_rest_day")
