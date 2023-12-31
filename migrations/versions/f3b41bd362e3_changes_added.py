"""changes added

Revision ID: f3b41bd362e3
Revises: c6fe057e93fe
Create Date: 2023-11-10 05:27:07.002264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3b41bd362e3'
down_revision = 'c6fe057e93fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('received_purchases', schema=None) as batch_op:
        batch_op.drop_index('status')

    with op.batch_alter_table('stock_orders', schema=None) as batch_op:
        batch_op.drop_index('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock_orders', schema=None) as batch_op:
        batch_op.create_index('status', ['status'], unique=False)

    with op.batch_alter_table('received_purchases', schema=None) as batch_op:
        batch_op.create_index('status', ['status'], unique=False)

    # ### end Alembic commands ###
