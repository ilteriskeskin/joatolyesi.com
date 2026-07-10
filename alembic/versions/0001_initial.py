"""Phase 1 initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-10
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "waitlist",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("lang", sa.String(5), nullable=False),
        sa.Column("source", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_waitlist_email", "waitlist", ["email"], unique=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("password_hash", sa.String(100), nullable=False),
        sa.Column("lang", sa.String(5), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True),
        sa.Column("ls_subscription_id", sa.String(50), nullable=False, unique=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("variant_name", sa.String(50), nullable=True),
        sa.Column("renews_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "practice_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("practiced_on", sa.Date(), nullable=False),
        sa.Column("discipline", sa.String(20), nullable=False),
        sa.Column("minutes", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_practice_logs_user_id", "practice_logs", ["user_id"])
    op.create_index("ix_practice_logs_practiced_on", "practice_logs", ["practiced_on"])

    op.create_table(
        "katas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("discipline", sa.String(20), nullable=False),
        sa.Column("title_en", sa.String(120), nullable=False),
        sa.Column("title_tr", sa.String(120), nullable=False),
        sa.Column("description_en", sa.Text(), nullable=False),
        sa.Column("description_tr", sa.Text(), nullable=False),
        sa.Column("video_url", sa.String(500), nullable=True),
        sa.Column("is_free", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
    )

    op.create_table(
        "programs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("title_en", sa.String(120), nullable=False),
        sa.Column("title_tr", sa.String(120), nullable=False),
        sa.Column("description_en", sa.Text(), nullable=False),
        sa.Column("description_tr", sa.Text(), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("is_published", sa.Boolean(), nullable=False),
    )

    op.create_table(
        "program_days",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("program_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("programs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("day_number", sa.Integer(), nullable=False),
        sa.Column("title_en", sa.String(120), nullable=False),
        sa.Column("title_tr", sa.String(120), nullable=False),
        sa.Column("content_en", sa.Text(), nullable=False),
        sa.Column("content_tr", sa.Text(), nullable=False),
        sa.Column("video_url", sa.String(500), nullable=True),
        sa.UniqueConstraint("program_id", "day_number"),
    )
    op.create_index("ix_program_days_program_id", "program_days", ["program_id"])

    op.create_table(
        "enrollments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("program_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("programs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("started_on", sa.Date(), nullable=False, server_default=sa.text("CURRENT_DATE")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", "program_id"),
    )
    op.create_index("ix_enrollments_user_id", "enrollments", ["user_id"])
    op.create_index("ix_enrollments_program_id", "enrollments", ["program_id"])

    op.create_table(
        "enrollment_days",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("enrollment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("day_number", sa.Integer(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("enrollment_id", "day_number"),
    )
    op.create_index("ix_enrollment_days_enrollment_id", "enrollment_days", ["enrollment_id"])


def downgrade() -> None:
    op.drop_table("enrollment_days")
    op.drop_table("enrollments")
    op.drop_table("program_days")
    op.drop_table("programs")
    op.drop_table("katas")
    op.drop_table("practice_logs")
    op.drop_table("subscriptions")
    op.drop_table("users")
    op.drop_table("waitlist")
