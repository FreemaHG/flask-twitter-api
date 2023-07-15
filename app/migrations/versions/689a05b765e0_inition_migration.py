"""inition migration

Revision ID: 689a05b765e0
Revises: 
Create Date: 2023-07-15 19:33:12.481317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689a05b765e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('nickname')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nickname', sa.VARCHAR(), nullable=False))

    # ### end Alembic commands ###
