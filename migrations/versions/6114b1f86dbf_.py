"""empty message

Revision ID: 6114b1f86dbf
Revises: 106c8f32b86a
Create Date: 2019-10-23 18:15:47.711926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6114b1f86dbf'
down_revision = '106c8f32b86a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('front_user',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('telephone', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('_password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('realname', sa.String(length=50), nullable=True),
    sa.Column('avatar', sa.String(length=100), nullable=True),
    sa.Column('signatuer', sa.String(length=100), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'SECRET', 'UNKNOW', name='genderenum'), nullable=True),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('telephone')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('front_user')
    # ### end Alembic commands ###
