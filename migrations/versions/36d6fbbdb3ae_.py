"""empty message

Revision ID: 36d6fbbdb3ae
Revises: e2d5b1fd9171
Create Date: 2021-12-22 15:57:23.044272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36d6fbbdb3ae'
down_revision = 'e2d5b1fd9171'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_comment')
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('comment')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.TEXT(), nullable=False))

    op.create_table('_alembic_tmp_comment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('create_date', sa.DATETIME(), nullable=False),
    sa.Column('modify_date', sa.DATETIME(), nullable=True),
    sa.Column('question_id', sa.INTEGER(), nullable=True),
    sa.Column('answer_id', sa.INTEGER(), nullable=True),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], name='fk_comment_answer_id_answer', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name='fk_comment_question_id_question', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_comment_user_id_user', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='pk_comment')
    )
    # ### end Alembic commands ###