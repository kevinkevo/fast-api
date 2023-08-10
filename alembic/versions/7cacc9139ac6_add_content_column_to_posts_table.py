"""add content column to posts table

Revision ID: 7cacc9139ac6
Revises: bd6aab58cd5c
Create Date: 2023-04-19 16:01:29.314914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cacc9139ac6'
down_revision = 'bd6aab58cd5c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content", sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
