"""empty message

Revision ID: bff61514b22e
Revises: be1f50e45f25
Create Date: 2024-12-15 12:06:14.973185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bff61514b22e'
down_revision = 'be1f50e45f25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ski_color', sa.String(length=50), nullable=True))
        batch_op.drop_column('ski_colo')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ski_colo', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.drop_column('ski_color')

    # ### end Alembic commands ###
