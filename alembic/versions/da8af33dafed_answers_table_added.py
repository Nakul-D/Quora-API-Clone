"""answers table added

Revision ID: da8af33dafed
Revises: 672c805353ec
Create Date: 2022-07-07 06:32:51.549456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da8af33dafed'
down_revision = '672c805353ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answers',
    sa.Column('answerId', sa.Integer(), nullable=False),
    sa.Column('questionId', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('createTime', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('lastUpdated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('edited', sa.Boolean(), server_default='False', nullable=False),
    sa.ForeignKeyConstraint(['questionId'], ['questions.questionId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['userId'], ['users.userId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('answerId')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers')
    # ### end Alembic commands ###