"""Kata/teknik ayrımı: katas.kind kolonu

Revision ID: 0008
Revises: 0007
"""

import sqlalchemy as sa
from alembic import op

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "katas",
        sa.Column("kind", sa.String(10), nullable=False, server_default="kata"),
    )


def downgrade() -> None:
    op.drop_column("katas", "kind")
