"""create posts table

Revision ID: bd6aab58cd5c
Revises: 
Create Date: 2023-04-19 15:34:10.270430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd6aab58cd5c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id",sa.Integer(),nullable=False,
                                       primary_key=True), sa.Column("title", sa.String(),nullable=False))
    
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
