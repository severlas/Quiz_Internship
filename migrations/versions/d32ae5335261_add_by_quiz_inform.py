"""add by_quiz inform

Revision ID: d32ae5335261
Revises: e1f2c4cb1e4f
Create Date: 2022-10-30 20:47:54.059483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd32ae5335261'
down_revision = 'e1f2c4cb1e4f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quiz_results', sa.Column('sum_questions_by_quiz', sa.Integer(), nullable=False))
    op.add_column('quiz_results', sa.Column('sum_correct_answers_by_quiz', sa.Integer(), nullable=False))
    op.add_column('quiz_results', sa.Column('gpa_by_quiz', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quiz_results', 'gpa_by_quiz')
    op.drop_column('quiz_results', 'sum_correct_answers_by_quiz')
    op.drop_column('quiz_results', 'sum_questions_by_quiz')
    # ### end Alembic commands ###