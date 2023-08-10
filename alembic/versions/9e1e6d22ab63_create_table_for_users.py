"""create table for users

Revision ID: 9e1e6d22ab63
Revises: 7cacc9139ac6
Create Date: 2023-04-19 16:20:24.748532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e1e6d22ab63'
down_revision = '7cacc9139ac6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(),nullable=False),
                    sa.Column("email", sa.String(),nullable=False),
                    sa.Column("password", sa.String(),nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                    server_default=sa.text("now()"),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    
    
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
