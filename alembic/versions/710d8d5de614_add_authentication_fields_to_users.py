"""add authentication fields to users

Revision ID: 710d8d5de614
Revises: bbb19c760733
Create Date: 2026-09-22 06:57:41.128659
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "710d8d5de614"
down_revision: Union[str, Sequence[str], None] = "bbb19c760733"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the password hash required for authenticated users."""
    op.add_column("users", sa.Column("hashed_password", sa.String(), nullable=False))


def downgrade() -> None:
    """Remove the authentication field added by this revision."""
    op.drop_column("users", "hashed_password")