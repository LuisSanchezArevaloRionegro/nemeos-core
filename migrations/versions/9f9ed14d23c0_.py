"""empty message

Revision ID: 9f9ed14d23c0
Revises: 1cb67a97abaf
Create Date: 2020-08-06 18:18:48.521808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f9ed14d23c0'
down_revision = '1cb67a97abaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercises', sa.Column('type', sa.String(length=80), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exercises', 'type')
    # ### end Alembic commands ###
