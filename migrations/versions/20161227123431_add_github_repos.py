# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b068ed4d85b2'
down_revision = 'c6450b9b01be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('github_repos',
    sa.Column('id', sa.Unicode(), nullable=False),
    sa.Column('owner', sa.Unicode(), nullable=False),
    sa.Column('repo', sa.Unicode(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_github_repos',
    sa.Column('user_id', sa.Unicode(), nullable=True),
    sa.Column('github_repo_id', sa.Unicode(), nullable=True),
    sa.ForeignKeyConstraint(['github_repo_id'], ['github_repos.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_github_repos')
    op.drop_table('github_repos')
    # ### end Alembic commands ###
