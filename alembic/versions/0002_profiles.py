"""User profiles: username, bio, discipline, public flag

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-10
"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(30), nullable=True))
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.add_column("users", sa.Column("display_name", sa.String(80), nullable=True))
    op.add_column("users", sa.Column("bio", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("discipline", sa.String(20), nullable=False, server_default="jo"))
    op.add_column("users", sa.Column("is_public", sa.Boolean(), nullable=False, server_default="false"))


def downgrade() -> None:
    op.drop_column("users", "is_public")
    op.drop_column("users", "discipline")
    op.drop_column("users", "bio")
    op.drop_column("users", "display_name")
    op.drop_index("ix_users_username", "users")
    op.drop_column("users", "username")
