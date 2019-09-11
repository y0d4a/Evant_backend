"""empty message

Revision ID: e7f10da65bd5
Revises: 
Create Date: 2019-09-11 15:18:55.327598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f10da65bd5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_preferences',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('preference', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('user_id', 'event_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_preferences')
    # ### end Alembic commands ###
