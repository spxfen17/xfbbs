"""empty message

Revision ID: cdc4badafdbf
Revises: bf250b4cb287
Create Date: 2019-11-27 17:42:58.618326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cdc4badafdbf'
down_revision = 'bf250b4cb287'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_ibfk_2', 'post', type_='foreignkey')
    op.drop_column('post', 'author_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author_id', mysql.VARCHAR(length=100), nullable=True))
    op.create_foreign_key('post_ibfk_2', 'post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###