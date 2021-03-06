# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3a19aabb983'
down_revision = '0be4daf96ecd'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('github_repos_users')
    op.drop_table('github_repos')


def downgrade():
    op.create_table(
        'github_repos',
        sa.Column('id', sa.Unicode(), nullable=False),
        sa.Column('owner', sa.Unicode(), nullable=False),
        sa.Column('repo', sa.Unicode(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('updated', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'github_repos_users',
        sa.Column('github_repo_id', sa.Unicode(), nullable=False),
        sa.Column('user_id', sa.Unicode(), nullable=False),
        sa.ForeignKeyConstraint(
            ['github_repo_id'], ['github_repos.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('github_repo_id', 'user_id')
    )
