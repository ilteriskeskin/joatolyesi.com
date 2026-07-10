"""Branş taksonomisi genişledi: jo -> aikijo, kata -> other

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-10
"""
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE users SET discipline = 'aikijo' WHERE discipline = 'jo'")
    op.execute("UPDATE users SET discipline = 'other' WHERE discipline = 'kata'")
    op.execute("UPDATE practice_logs SET discipline = 'aikijo' WHERE discipline = 'jo'")
    op.execute("UPDATE practice_logs SET discipline = 'other' WHERE discipline = 'kata'")
    op.alter_column("users", "discipline", server_default="aikijo")


def downgrade() -> None:
    op.execute("UPDATE users SET discipline = 'jo' WHERE discipline = 'aikijo'")
    op.execute("UPDATE practice_logs SET discipline = 'jo' WHERE discipline = 'aikijo'")
    op.alter_column("users", "discipline", server_default="jo")
