"""rating

Revision ID: 1509b1506513
Revises: 230c6ac3dc59
Create Date: 2023-11-10 21:07:48.423704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1509b1506513'
down_revision = '230c6ac3dc59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating')
    # ### end Alembic commands ###
