"""create devices and loans tables

Revision ID: bbb19c760733
Revises: 73e8186e81d4
Create Date: 2026-09-17
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bbb19c760733"
down_revision: Union[str, Sequence[str], None] = "73e8186e81d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create devices and loans tables."""

    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("serial_number", sa.String(), nullable=False),
        sa.Column("device_type", sa.String(), nullable=False),
        sa.Column("brand", sa.String(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_devices_id",
        "devices",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_devices_serial_number",
        "devices",
        ["serial_number"],
        unique=True,
    )

    op.create_table(
        "loans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("loan_date", sa.DateTime(), nullable=False),
        sa.Column("return_date", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_loans_id",
        "loans",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop devices and loans tables."""

    op.drop_index("ix_loans_id", table_name="loans")
    op.drop_table("loans")

    op.drop_index(
        "ix_devices_serial_number",
        table_name="devices",
    )
    op.drop_index(
        "ix_devices_id",
        table_name="devices",
    )
    op.drop_table("devices")