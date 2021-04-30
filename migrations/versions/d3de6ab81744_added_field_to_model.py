"""Added field to model

Revision ID: d3de6ab81744
Revises: 7554c9905d81
Create Date: 2021-03-04 15:44:13.531670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3de6ab81744'
down_revision = '7554c9905d81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('to', sa.String(length=100), nullable=False),
    sa.Column('sender', sa.String(length=100), nullable=False),
    sa.Column('subject', sa.String(length=300), nullable=False),
    sa.Column('body', sa.String(length=8000), nullable=False),
    sa.Column('date_sent', sa.DateTime(), nullable=False),
    sa.Column('date_received', sa.DateTime(), nullable=False),
    sa.Column('naive_bayes_spam', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email')
    # ### end Alembic commands ###
