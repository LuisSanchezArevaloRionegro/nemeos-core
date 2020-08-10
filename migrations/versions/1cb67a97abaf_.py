"""empty message

Revision ID: 1cb67a97abaf
Revises: 802eae9ffcf7
Create Date: 2020-08-06 18:02:58.421181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cb67a97abaf'
down_revision = '802eae9ffcf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('material',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('material')
    # ### end Alembic commands ###