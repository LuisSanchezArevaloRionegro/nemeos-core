"""empty message

Revision ID: a4565f78b379
Revises: 
Create Date: 2020-07-30 18:36:51.762854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4565f78b379'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exercise_workout',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=True),
    sa.Column('workout_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exercise_workout')
    # ### end Alembic commands ###
