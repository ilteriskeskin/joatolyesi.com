"""Aktif program seçimi: enrollments.activated_at (B-41a)

Mevcut kayıtlar created_at ile doldurulur: bugünkü "en son kayıt aktif" davranışı korunur.

Revision ID: 0013
Revises: 0012
"""

import sqlalchemy as sa
from alembic import op

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "enrollments",
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.execute("UPDATE enrollments SET activated_at = created_at WHERE created_at IS NOT NULL")


def downgrade() -> None:
    op.drop_column("enrollments", "activated_at")
