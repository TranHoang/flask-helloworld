"""empty message

Revision ID: 0d9e4173fb5b
Revises: bacad44ae747
Create Date: 2018-09-10 14:20:19.361845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d9e4173fb5b'
down_revision = 'bacad44ae747'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('updated', sa.DateTime(), nullable=True))
        batch_op.drop_column('created_date')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('updated', sa.DateTime(), nullable=True))
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DATETIME(), nullable=True))
        batch_op.drop_column('updated')
        batch_op.drop_column('created')

    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DATETIME(), nullable=True))
        batch_op.drop_column('updated')
        batch_op.drop_column('created')

    # ### end Alembic commands ###