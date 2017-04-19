"""empty message

Revision ID: 7c50c9d84f90
Revises: b06bf7dc7fcb
Create Date: 2017-04-17 23:30:25.307992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c50c9d84f90'
down_revision = 'b06bf7dc7fcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.Column('attending', sa.Integer(), nullable=True),
    sa.Column('noreply', sa.Integer(), nullable=True),
    sa.Column('declined', sa.Integer(), nullable=True),
    sa.Column('maybe', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_time', sa.String(), nullable=True),
    sa.Column('end_time', sa.String(), nullable=True),
    sa.Column('profile_picture', sa.String(), nullable=True),
    sa.Column('cover_picture', sa.String(), nullable=True),
    sa.Column('time_from_now', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    # ### end Alembic commands ###
