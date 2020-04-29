"""create and update time

Revision ID: 3f49b98b1a24
Revises: bdd6a87edd97
Create Date: 2020-04-29 06:20:10.875343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f49b98b1a24'
down_revision = 'bdd6a87edd97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('createTime', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('lastModified', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lastModified')
    op.drop_column('users', 'createTime')
    # ### end Alembic commands ###