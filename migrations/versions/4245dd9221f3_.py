"""empty message

Revision ID: 4245dd9221f3
Revises: 
Create Date: 2024-06-21 20:48:50.846890

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4245dd9221f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('filename', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['uid'], ['users.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('parent_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('user_id', sa.BigInteger(), nullable=False))
        batch_op.drop_column('last_cid')
        batch_op.drop_column('comment')
        batch_op.drop_column('level')
        batch_op.drop_column('cid')
        batch_op.drop_column('uid')
        batch_op.drop_column('time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', mysql.VARCHAR(length=40), nullable=False))
        batch_op.add_column(sa.Column('uid', mysql.BIGINT(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('cid', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('level', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('comment', mysql.TEXT(), nullable=False))
        batch_op.add_column(sa.Column('last_cid', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('user_id')
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('content')
        batch_op.drop_column('parent_id')
        batch_op.drop_column('id')

    op.drop_table('videos')
    # ### end Alembic commands ###
