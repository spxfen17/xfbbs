"""empty message

Revision ID: e30db1313aeb
Revises: 64a08d83339d
Create Date: 2019-11-10 16:14:04.694167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e30db1313aeb'
down_revision = '64a08d83339d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('banner', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('banner', 'create_time')
    # ### end Alembic commands ###