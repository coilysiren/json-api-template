"""user table

Revision ID: b39c2bfdd80a
Revises:
Create Date: 2020-04-28 02:25:02.753499

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b39c2bfdd80a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###