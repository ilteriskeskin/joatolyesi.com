"""Kayıtlı kullanıcılar için davet linki (referral_code / referred_by)

Revision ID: 0010
Revises: 0009
"""

import sqlalchemy as sa
from alembic import op

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("referral_code", sa.String(12), nullable=True))
    op.add_column("users", sa.Column("referred_by", sa.String(12), nullable=True))
    op.create_index("ix_users_referral_code", "users", ["referral_code"], unique=True)
    op.create_index("ix_users_referred_by", "users", ["referred_by"])
    # Mevcut kullanıcılara benzersiz kod üret (id'nin ilk 10 hex karakteri — zaten benzersiz)
    op.execute("UPDATE users SET referral_code = substr(replace(id::text, '-', ''), 1, 10) WHERE referral_code IS NULL")
    op.alter_column("users", "referral_code", nullable=False)


def downgrade() -> None:
    op.drop_index("ix_users_referred_by", table_name="users")
    op.drop_index("ix_users_referral_code", table_name="users")
    op.drop_column("users", "referred_by")
    op.drop_column("users", "referral_code")
