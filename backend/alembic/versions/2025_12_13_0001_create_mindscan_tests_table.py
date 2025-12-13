"""create mindscan tests table

Revision ID: 2025_12_13_0001
Revises: 
Create Date: 2025-12-13
"""

from alembic import op
import sqlalchemy as sa

revision = "2025_12_13_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "mindscan_tests",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("subject_id", sa.String(length=64), nullable=False),
        sa.Column("results", sa.JSON, nullable=False),
    )


def downgrade():
    op.drop_table("mindscan_tests")
