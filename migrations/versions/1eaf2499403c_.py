"""empty message

Revision ID: 1eaf2499403c
Revises: None
Create Date: 2015-05-02 17:13:40.503454

"""

# revision identifiers, used by Alembic.
revision = '1eaf2499403c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('netid', sa.String(length=15), nullable=False),
    sa.Column('full_name', sa.String(length=200), nullable=True),
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=200), nullable=True),
    sa.Column('number_of_roommates', sa.SmallInteger(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('time_period', sa.SmallInteger(), nullable=True),
    sa.Column('grad_year', sa.SmallInteger(), nullable=True),
    sa.Column('searching', sa.Boolean(), nullable=True),
    sa.Column('email_updates', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('netid')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###
