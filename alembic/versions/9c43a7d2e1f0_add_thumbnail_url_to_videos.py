"""add thumbnail url to videos

Revision ID: 9c43a7d2e1f0
Revises: 3857227e9239
Create Date: 2026-11-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9c43a7d2e1f0"
down_revision: Union[str, Sequence[str], None] = "3857227e9239"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "videos",
        sa.Column("thumbnail_url", sa.String(length=1000), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("videos", "thumbnail_url")
