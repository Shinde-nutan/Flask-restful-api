"""changes in cloumn

Revision ID: 230c6ac3dc59
Revises: 5befe185ca46
Create Date: 2023-11-09 10:11:53.983602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '230c6ac3dc59'
down_revision = '5befe185ca46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(), nullable=True))
        batch_op.drop_column('is_admin')
        batch_op.drop_column('is_movie_creator')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_movie_creator', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('is_admin', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('role')

    # ### end Alembic commands ###