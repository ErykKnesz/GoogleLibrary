"""books table

Revision ID: 920f062b8d67
Revises: 
Create Date: 2021-08-13 21:12:02.926376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '920f062b8d67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('author', sa.String(length=80), nullable=False),
    sa.Column('published_date', sa.DateTime(), nullable=False),
    sa.Column('ISBN', sa.Integer(), nullable=False),
    sa.Column('num_pages', sa.Integer(), nullable=False),
    sa.Column('cover_url', sa.Text(), nullable=False),
    sa.Column('language', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###
