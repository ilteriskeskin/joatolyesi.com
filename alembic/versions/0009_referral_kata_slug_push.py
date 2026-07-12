"""Waitlist referans linki, kata tekrar sayacı, push abonelikleri

Revision ID: 0009
Revises: 0008
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Waitlist: referans kodu + kimin getirdiği
    op.add_column("waitlist", sa.Column("referral_code", sa.String(12), nullable=True))
    op.add_column("waitlist", sa.Column("referred_by", sa.String(12), nullable=True))
    op.create_index("ix_waitlist_referral_code", "waitlist", ["referral_code"], unique=True)
    op.create_index("ix_waitlist_referred_by", "waitlist", ["referred_by"])
    # Mevcut kayıtlara benzersiz kod üret (id'nin ilk 10 hex karakteri — zaten benzersiz)
    op.execute("UPDATE waitlist SET referral_code = substr(replace(id::text, '-', ''), 1, 10) WHERE referral_code IS NULL")
    op.alter_column("waitlist", "referral_code", nullable=False)

    # Kata tekrar sayacı
    op.add_column("practice_logs", sa.Column("kata_slug", sa.String(80), nullable=True))
    op.create_index("ix_practice_logs_kata_slug", "practice_logs", ["kata_slug"])

    # Push abonelikleri
    op.create_table(
        "push_subscriptions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("endpoint", sa.String(500), nullable=False, unique=True),
        sa.Column("p256dh", sa.String(200), nullable=False),
        sa.Column("auth", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("push_subscriptions")
    op.drop_index("ix_practice_logs_kata_slug", table_name="practice_logs")
    op.drop_column("practice_logs", "kata_slug")
    op.drop_index("ix_waitlist_referred_by", table_name="waitlist")
    op.drop_index("ix_waitlist_referral_code", table_name="waitlist")
    op.drop_column("waitlist", "referred_by")
    op.drop_column("waitlist", "referral_code")
