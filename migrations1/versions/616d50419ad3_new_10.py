"""new 10.

Revision ID: 616d50419ad3
Revises: ce219dcc9e28
Create Date: 2024-04-15 22:08:07.206924

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '616d50419ad3'
down_revision = 'ce219dcc9e28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('timeline', schema=None) as batch_op:
        batch_op.drop_column('apply_job')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('timeline', schema=None) as batch_op:
        batch_op.add_column(sa.Column('apply_job', postgresql.ENUM('apply_status', name='apply_status'), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
