# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '1ad9f7550e9e'
down_revision = '764d8a0341e3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Unicode(), nullable=False),
        sa.Column('name', sa.Unicode(), nullable=False),
        sa.Column('email', sa.Unicode(), nullable=False),
        sa.Column('display_name', sa.Unicode(), nullable=True),
        sa.Column('created', sa.DateTime(timezone=True), nullable=True),
        sa.Column('admin', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('name')
    )


def downgrade():
    op.drop_table('users')
