"""empty message

Revision ID: 98430fc806aa
Revises: 9f9ed14d23c0
Create Date: 2020-08-06 18:28:17.348817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98430fc806aa'
down_revision = '9f9ed14d23c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercises', sa.Column('name_en', sa.String(length=80), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exercises', 'name_en')
    # ### end Alembic commands ###
