"""empty message

Revision ID: d7d6ebf628
Revises: 199674c8eb82
Create Date: 2015-05-05 16:15:54.262573

"""

# revision identifiers, used by Alembic.
revision = 'd7d6ebf628'
down_revision = '199674c8eb82'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('number_of_roommates')

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number_of_roommates', sa.SMALLINT(), nullable=True))

    ### end Alembic commands ###
