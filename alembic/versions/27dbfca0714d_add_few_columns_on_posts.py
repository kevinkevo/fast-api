"""add few columns on posts

Revision ID: 27dbfca0714d
Revises: 58974e039939
Create Date: 2023-04-19 17:08:36.406484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27dbfca0714d'
down_revision = '58974e039939'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                    server_default=sa.text("now()"),nullable=False))

    pass


def downgrade() -> None:
    op.drop_column("posts","created_at")
    pass
