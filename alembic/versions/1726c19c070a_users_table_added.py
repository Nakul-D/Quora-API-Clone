"""users table added

Revision ID: 1726c19c070a
Revises: 
Create Date: 2022-06-29 05:43:49.082766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1726c19c070a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('createTime', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('lastUpdated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('userId'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
