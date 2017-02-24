"""Add UserPreferences

Revision ID: 20cb28a89cc6
Revises: 498a6d3a1e0f
Create Date: 2015-10-17 18:20:11.865650

"""

# revision identifiers, used by Alembic.
revision = '20cb28a89cc6'
down_revision = u'498a6d3a1e0f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'UserPreferences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('labs_sort_method', sa.Unicode(length=32), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], [u'User.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine=u'InnoDB'
    )
    op.create_index(u'ix_UserPreferences_user_id', u'UserPreferences', ['user_id'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(u'ix_UserPreferences_user_id', table_name=u'UserPreferences')
    op.drop_table(u'UserPreferences')
    ### end Alembic commands ###
