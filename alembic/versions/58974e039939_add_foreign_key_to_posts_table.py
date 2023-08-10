"""add foreign-key to posts table

Revision ID: 58974e039939
Revises: 9e1e6d22ab63
Create Date: 2023-04-19 16:46:11.487358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58974e039939'
down_revision = '9e1e6d22ab63'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id", sa.Integer(),nullable=False))
    op.create_foreign_key("post_users_fk",source_table="posts",referent_table="users",
                          local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts","owner_id")
    pass
