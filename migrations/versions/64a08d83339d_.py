"""empty message

Revision ID: 64a08d83339d
Revises: 4dedbba328c5
Create Date: 2019-11-10 16:13:50.798250

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '64a08d83339d'
down_revision = '4dedbba328c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('banner', 'create_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('banner', sa.Column('create_time', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###