"""empty message

Revision ID: c6d590a114d2
Revises: aa886063666a
Create Date: 2019-07-29 14:04:51.540430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6d590a114d2'
down_revision = 'aa886063666a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('first_name', sa.String(length=120), nullable=True))
    op.add_column('Users', sa.Column('last_name', sa.String(length=120), nullable=True))
    op.add_column('Users', sa.Column('password', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'password')
    op.drop_column('Users', 'last_name')
    op.drop_column('Users', 'first_name')
    # ### end Alembic commands ###
