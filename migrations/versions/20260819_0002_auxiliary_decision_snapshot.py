"""Persistir snapshot de decision auxiliar.

Revision ID: 20260819_0002
Revises: 20260811_0001
Create Date: 2026-08-19
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260819_0002"
down_revision: Union[str, Sequence[str], None] = "20260811_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "Evaluations",
        sa.Column("auxiliary_decision_json", sa.Text(), nullable=True),
        schema="dbo",
    )


def downgrade() -> None:
    op.drop_column("Evaluations", "auxiliary_decision_json", schema="dbo")
